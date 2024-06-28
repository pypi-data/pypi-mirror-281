# coding=utf-8
# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom application related commands"""

from __future__ import print_function

import os
from multiprocessing import Process, cpu_count
from time import time
import sys
import zipfile
import shutil
import xml.etree.ElementTree as ET
import contextlib
from knack.util import CLIError
import joblib
from joblib import Parallel, delayed
from tqdm import tqdm
from sfctl.custom_exceptions import SFCTLInternalException
from sfctl.util import get_user_confirmation

@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    #pylint: disable=useless-super-delegation,too-few-public-methods
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        """
        tqdm class callback overrides to enable usage with Parallel loop
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()

def validate_app_path(app_path):
    """Validate and return application package as absolute path"""

    abspath = os.path.abspath(app_path)
    if os.path.isdir(abspath):
        return abspath

    raise ValueError(
        'Invalid path to application directory: {0}'.format(abspath)
    )

def print_progress(current, total, rel_file_path, show_progress, time_left=None):
    """Display progress for uploading"""
    if show_progress:
        print(
            '[{}/{}] files, {}'.format(current, total, rel_file_path),
            file=sys.stderr
        )
        if time_left is not None:
            print('Time left: {} seconds'.format(time_left))

def path_from_imagestore_string(imagestore_connstr):
    """
    Parse the file share path from the image store connection string
    """
    if imagestore_connstr and 'file:' in imagestore_connstr:
        conn_str_list = imagestore_connstr.split("file:")
        return conn_str_list[1]
    return False

def get_job_count():
    """
    Test-mockable wrapper for returning cpu count.
    """
    jobcount = None
    try:
        jobcount = cpu_count()
    except Exception as ex: #pylint: disable=broad-except
        print('Warning: cpu_count hit exception {}. Defaulting to 1.'.format(ex))
        jobcount = 1

    if jobcount is None:
        jobcount = 2
    return jobcount

def upload_to_fileshare(source, dest, show_progress):
    """
    Copies the package from source folder to dest folder
    """
    total_files_count = 0
    current_files_count = 0
    for root, _, files in os.walk(source):
        total_files_count += len(files)

    for root, _, files in os.walk(source):
        for single_file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path)
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)

            shutil.copyfile(
                os.path.join(root, single_file), os.path.join(dest_path, single_file)
            )
            current_files_count += 1
            print_progress(current_files_count, total_files_count,
                           os.path.normpath(os.path.join(rel_path, single_file)),
                           show_progress)

    if show_progress:
        print('Complete', file=sys.stderr)

def get_timeout_left(target_timeout):
    """
    Return the number of seconds until timeout is reached, given a target_timeout which represents
      the time at which the timer should stop. If the time left is less than 0, return 0
    :param target_timeout: time measured as from epoch in seconds
    :return: int
    """
    current_time = int(time())  # time from epoch in seconds
    time_left = target_timeout - current_time

    if time_left <= 0:
        return 0
    return time_left

def get_lesser(num_a, num_b):
    """
    Return the lesser of int num_a and int num_b. If the lesser number is less than 0, return 0
    :param num_a: (int)
    :param num_b: (int)
    :return: Return the smaller of num_a or num_b.
    """

    return max(0, min(num_a, num_b))

def upload_single_file_native_imagestore(sesh, endpoint, basename, #pylint: disable=too-many-locals,too-many-arguments
                                         rel_path, single_file, root, target_timeout):
    """
    Used by upload_to_native_imagestore to upload individual files
    of the application package to cluster

    :param sesh: A requests (module) session object.
    :param endpoint: Connection url endpoint for upload requests.
    :param basename: Image store base path.
    :param rel_path: Image store relative directory path.
    :param single_file: Filename.
    :param root: Source directory path.
    :param target_timeout: Time at which timeout would be reached.
    """
    try:
        from urllib.parse import urlparse, urlencode, urlunparse
    except ImportError:
        from urllib import urlencode
        from urlparse import urlparse, urlunparse  # pylint: disable=import-error

    current_time_left = get_timeout_left(target_timeout)   # an int representing seconds

    if current_time_left == 0:
        raise SFCTLInternalException('Upload has timed out. Consider passing a longer '
                                        'timeout duration.')

    url_path = (
        os.path.normpath(os.path.join('ImageStore', basename,
                                        rel_path, single_file))
    ).replace('\\', '/')
    fp_norm = os.path.normpath(os.path.join(root, single_file))
    with open(fp_norm, 'rb') as file_opened:
        url_parsed = list(urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urlencode(
            {'api-version': '6.1',
                'timeout': current_time_left})
        url = urlunparse(url_parsed)

        # timeout is (connect_timeout, read_timeout)
        res = sesh.put(url, data=file_opened,
                        timeout=(get_lesser(60, current_time_left), current_time_left))

        res.raise_for_status()

def upload_to_native_imagestore(sesh, endpoint, abspath, basename, #pylint: disable=too-many-locals,too-many-arguments
                                show_progress, timeout):
    """
    Upload the application package to cluster

    :param sesh: A requests (module) session object.
    :param endpoint: Connection url endpoint for upload requests.
    :param abspath: Application source path.
    :param basename: Image store destination path.
    :param show_progress: boolean to determine whether to log upload progress.
    :param timeout: Total upload timeout in seconds.
    """

    try:
        from urllib.parse import urlparse, urlencode, urlunparse
    except ImportError:
        from urllib import urlencode
        from urlparse import urlparse, urlunparse  # pylint: disable=import-error
    total_files_count = 0
    current_files_count = 0
    for root, _, files in os.walk(abspath):
        # Number of uploads is number of files plus number of directories
        total_files_count += (len(files) + 1)

    target_timeout = int(time()) + timeout
    jobcount = get_job_count()

    # Note: while we are raising some exceptions regarding upload timeout, we are leaving the
    # timeouts raised by the requests library as is since it contains enough information
    for root, _, files in os.walk(abspath):
        rel_path = os.path.normpath(os.path.relpath(root, abspath))
        filecount = len(files)

        try:
            if show_progress:
                progressdescription = 'Uploading path: {}'.format(rel_path)
                with tqdm_joblib(tqdm(desc=progressdescription, total=filecount)):
                    Parallel(n_jobs=jobcount)(
                        delayed(upload_single_file_native_imagestore)(
                            sesh, endpoint, basename, rel_path, single_file, root, target_timeout)
                            for single_file in files)
            else:
                Parallel(n_jobs=jobcount)(
                    delayed(upload_single_file_native_imagestore)(
                        sesh, endpoint, basename, rel_path, single_file, root, target_timeout)
                        for single_file in files)
        except Exception as e:
            print(e)
            raise SFCTLInternalException('Upload has timed out. Consider passing a longer '
                                         'timeout duration.')
        current_time_left = get_timeout_left(target_timeout)

        if current_time_left == 0:
            raise SFCTLInternalException('Upload has timed out. Consider passing a longer '
                                         'timeout duration.')

        url_path = (
            os.path.normpath(os.path.join('ImageStore', basename,
                                          rel_path, '_.dir'))
        ).replace('\\', '/')
        url_parsed = list(urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urlencode({'api-version': '6.1',
                                   'timeout': current_time_left})
        url = urlunparse(url_parsed)

        res = sesh.put(url,
                       timeout=(get_lesser(60, current_time_left), current_time_left))
        res.raise_for_status()
        current_files_count += filecount + 1
        print_progress(current_files_count, total_files_count,
                       os.path.normpath(os.path.join(rel_path, '_.dir')),
                       show_progress, get_timeout_left(target_timeout))
    if show_progress:
        print('Complete', file=sys.stderr)

class IgnoreCopy():  # pylint: disable=too-few-public-methods,bad-option-value,C1001
    """
    A class which contains information and methods for the shutil.copytree method's
    callback parameter.
    """

    def __init__(self):
        # Directories which will be ignored as part of the ignore_copy function
        # If used for compressing application package:
        # A list of strings representing the abs path of the dirs in an application package
        # which need to be compressed
        # Paths in dirs_to_ignore should normalized using the _normalize_path function before setting
        self.dirs_to_ignore = []

    def ignore_copy(self, directory_being_visited, list_of_dirs):
        """
        The ignore function for shutil.copytree()

        :param directory_being_visited: str
        :param list_of_dirs: Example: ['t.txt']

        :return: a subset of the items in its second argument (must be relative path).
                 these names will then be ignored in the copy process
        """

        to_ignore = []

        for directory in list_of_dirs:

            full_path = os.path.join(directory_being_visited, directory)
            full_path = _normalize_path(full_path)
            if full_path in self.dirs_to_ignore:
                to_ignore.append(directory)

        return to_ignore

def _normalize_path(path):
    """
    Standardize a path to a file/folder location so that they can be compared

    :param path: (str) represents a path on a machine
    :return: (str) the standardized path
    """

    path = os.path.realpath(path)  # This removes slashes at the end of the path
    path = os.path.normpath(path)
    path = os.path.normcase(path)
    path = os.path.abspath(path)
    return path

# Note: provide in place compress in the future
def compress_package(app_dir, output_dir):
    """
    Compress to the location passed in (output_dir). Note that it is not the entire package
    which is compressed, but rather, only some inside parts of the app package folder.

    Check if the folder has the correct structure for a service fabric application. If
    not, raise an exception alerting user of bad folder structure.

    ZIP64 functionality is present for Python
    versions 3.4 and above.

    For example, if app_dir = C:/SomeFolder/WordCountApp
    and if output_dir = C:/SomeLocation,
    then the following will be created: C:/SomeLocation/WordCountApp

    :param app_dir: (str) An absolute path to an application package to be compressed

    :param output_dir: (str) An absolute path to the location to output the zipped dir

    :return: Nothing, or a CLIError exception
    """

    # Check if we're dealing with a dir in _check_folder_structure_and_get_dirs instead of
    # in this function

    # Normalize slashes, etc, in app_dir and output_dir
    app_dir = _normalize_path(app_dir)
    output_dir = _normalize_path(output_dir)

    compress_copy = IgnoreCopy()

    # Exception will be raised if the package isn't the correct structure
    # This list may be empty in the case of an already compressed application package
    compress_copy.dirs_to_ignore = _check_folder_structure_and_get_dirs(app_dir)

    if not compress_copy.dirs_to_ignore:
        print("Nothing to copy")

    app_name = os.path.basename(app_dir)
    copy_output_path = os.path.join(output_dir, app_name)

    # Get the relative paths under app_name of dirs_to_copy so that we know
    # where to place the new zipped file
    relative_paths_to_compress = []
    for directory in compress_copy.dirs_to_ignore:

        rel_path = directory[len(app_dir):]
        relative_paths_to_compress.append(rel_path.lstrip('\\').lstrip('/'))

    try:
        # Copy everything except the one we want to zip. Those we will do manually
        shutil.copytree(app_dir, copy_output_path, ignore=compress_copy.ignore_copy)

        i = 0
        for directory in relative_paths_to_compress:

            dir_to_compress = compress_copy.dirs_to_ignore[i]

            # Example: shutil.make_archive('C:\\Users\\user\\Downloads\\Code', 'zip',
            # root_dir='C:\\WordCountV1Original\\WordCountServicePkg\\Code')
            # The above will copy the contents of root_dir into the path given as the first
            # parameter, with a .zip extension, so that a Code.zip will be created in Downloads

            # Note for python versions before 3.4, zipping of folders larger than 2GB isn't
            # supported
            # It is more work and code to support Python 2.7 for this, and since we do plan to
            # deprecate support for Python 2.7 in the future, we will just not add it here.
            shutil.make_archive(os.path.join(copy_output_path, directory), 'zip', dir_to_compress)

            i += 1

    except zipfile.LargeZipFile as ex:
        raise CLIError('Compression failed due to file too large. If you have Python 2.7, '
                       'upgrading to 3.5 or higher will fix the issue. Please clean up '
                       'location ' + output_dir + '\n' + str(ex))

    except Exception as ex:
        raise CLIError(str.format('Compression failed due to {0}. Please clean up '
                                  'location {1}', str(ex), output_dir))


def _check_folder_structure_and_get_dirs(app_dir):
    """
    Check if the given path is a folder. If not, raise an exception indicating only
    SF app package folders can be compressed.

    Check if the folder given corresponds to a valid application structure. If the package
    is valid, return a list of dirs (abs path, normalized using the
    _normalize_path function) to be compressed.

    If the folder is already compressed, then return empty list.

    Example format:

    WordCountApp (this is the last segment of the app_dir path)

        o WordCountServicePkg
              Code
            •     WordCount.Service.exe
            •     Other Files
              Config
            •     Settings.xml
              ServiceManifest.xml

        o WordCountWebServicePkg
              Code
            •     WordCount.WebService.exe
            •     Other Files
              Config
            •     Settings.xml
              ServiceManifest.xml

        o    ApplicationManifest.xml

    The Code and Config folders should be compressed. These will be listed in the Application and Service manifests.

    :param app_dir: (str) An absolute path to an application package
    :return: A list of strings representing the absolute paths to directories which should
             be compressed. Return a CLIError if the provided path is not a dir
    """

    # Future optimization: don't copy already compressed packages. Just let the user know
    # and upload. This should be an uncommon case, and isn't worth the effort now

    to_compress = []

    if not os.path.isdir(app_dir):
        raise CLIError('Only Service Fabric application packages may be compressed. '
                       'The following path is not a directory: ' + app_dir)

    path_to_app_manifest = os.path.join(app_dir, 'ApplicationManifest.xml')

    # An application manifest file should exist directly under the directory passed in
    if not os.path.isfile(path_to_app_manifest):  # Casing does not matter
        raise CLIError('Application package to be compressed is missing ApplicationManifest.xml')

    # A list of the service packages. This should be the absolute path
    service_packages = []

    # Parse the application manifest to find which folders should have the service manifest.
    app_manifest_parsed = ET.parse(path_to_app_manifest).getroot()
    for child in app_manifest_parsed:
        # Use ends with, because the tags start with the xmlns
        if child.tag.endswith('ServiceManifestImport'):
            # We expect a child element that looks like:
            # <ServiceManifestRef ServiceManifestName="CalculatorServicePackage" ServiceManifestVersion="1.0"/>
            for inner_child in child:
                if inner_child.tag.endswith('ServiceManifestRef'):
                    path_to_service_package = os.path.join(app_dir, inner_child.attrib.get('ServiceManifestName'))
                    service_packages.append(path_to_service_package)

    # Go through each service package folder and search for the service manifest
    # The service manifest defines which packages are the code, config, and data packages, which
    # needs to be compressed.
    for service_package_path in service_packages:
        path_to_service_manifest = os.path.join(service_package_path, 'ServiceManifest.xml')

        # Raise exception is the expected service manifest file doesn't exist AND
        # if the service package isn't already zipped
        if not os.path.isfile(path_to_service_manifest) \
                and not os.path.isfile(path_to_service_manifest+'.sfpkg'):  # Casing does not matter
            raise CLIError('Service package to be compressed is missing ServiceManifest.xml in ' + service_package_path)

        service_manifest_parsed = ET.parse(path_to_service_manifest).getroot()

        for child in service_manifest_parsed:
            if child.tag.endswith('CodePackage') or \
                    child.tag.endswith('ConfigPackage') or child.tag.endswith('DataPackage'):

                # If the app package already compressed,
                # then mark a bool somewhere that says that this package is already
                # compressed, and expect that we just upload the entire package without copying to any location
                # In this case, we would not copy to output dir, and just upload. For partially compressed,
                # we should compress just those and throw the compressed in the output folder
                # For the case where there is no copy needed, we should print a statement letting the user know.

                folder_name = child.attrib.get("Name")
                folder_to_compress = os.path.join(service_package_path, folder_name)

                if not os.path.isdir(folder_to_compress):  # Casing does not matter
                    raise CLIError(str.format("{0} defined in {1} does not exist",
                                              folder_to_compress, path_to_service_manifest))

                to_compress.append(_normalize_path(folder_to_compress))

    return to_compress

def upload(path, imagestore_string='fabric:ImageStore', show_progress=False, timeout=300,  # pylint: disable=too-many-locals,missing-docstring,too-many-arguments,too-many-branches,too-many-statements
           compress=False, keep_compressed=False, compressed_location=None):

    from sfctl.config import (client_endpoint, no_verify_setting, ca_cert_info,
                              cert_info)
    import requests

    path = _normalize_path(path)
    if compressed_location is not None:
        compressed_location = _normalize_path(compressed_location)

    abspath = validate_app_path(path)
    basename = os.path.basename(abspath)

    endpoint = client_endpoint()
    cert = cert_info()
    ca_cert = True
    if no_verify_setting():
        ca_cert = False
    elif ca_cert_info():
        ca_cert = ca_cert_info()

    if all([no_verify_setting(), ca_cert_info()]):
        raise CLIError('Cannot specify both CA cert info and no verify')

    if not compress and (keep_compressed or compressed_location is not None):
        raise CLIError('--keep-compressed and --compressed-location options are only applicable '
                       'if the --compress option is set')

    compressed_pkg_location = None
    created_dir_path = None

    if compress:

        parent_folder = os.path.dirname(path)
        file_or_folder_name = os.path.basename(path)

        compressed_pkg_location = os.path.join(parent_folder, 'sfctl_compressed_temp')

        if compressed_location is not None:
            compressed_pkg_location = compressed_location

        # Check if a zip file has already been created
        created_dir_path = os.path.join(compressed_pkg_location, file_or_folder_name)

        if os.path.exists(created_dir_path):
            if get_user_confirmation(str.format('Deleting previously generated compressed files at '
                                                '{0}. If this folder has anything else, those will be '
                                                'deleted as well. Allow? ["y", "n"]: ', created_dir_path)):
                shutil.rmtree(created_dir_path)
            else:
                # We can consider adding an option to number the packages in the future.
                print('Stopping upload operation. Cannot compress to the following location '
                      'because the path already exists: ' + created_dir_path)
                return

        # Let users know where to find the compressed app package before starting the
        # copy / compression, in case the process crashes in the middle, so users
        # will know where to clean up items from, or where to upload already compressed
        # app packages from
        if show_progress:
            print('Starting package compression into location: ' + compressed_pkg_location)
            print()  # New line for formatting purposes
        compress_package(path, compressed_pkg_location)

        # Change the path to the path with the compressed package
        compressed_path = os.path.join(compressed_pkg_location, file_or_folder_name)

        # re-do validation and reset the variables
        abspath = validate_app_path(compressed_path)
        basename = os.path.basename(abspath)

    # Note: pressing ctrl + C during upload does not end the current upload in progress, but only
    # stops the next one from occurring. This will be fixed in the future.

    # Upload to either to a folder, or native image store only
    if 'file:' in imagestore_string:
        dest_path = path_from_imagestore_string(imagestore_string)

        process = Process(target=upload_to_fileshare,
                          args=(abspath, os.path.join(dest_path, basename), show_progress))

        process.start()
        process.join(timeout)  # If timeout is None then there is no timeout.

        if process.is_alive():
            process.terminate()  # This will leave any children of process orphaned.
            raise SFCTLInternalException('Upload has timed out. Consider passing a longer '
                                         'timeout duration.')

    elif imagestore_string == 'fabric:ImageStore':

        with requests.Session() as sesh:
            sesh.verify = ca_cert
            sesh.cert = cert

            # There is no need for a new process here since
            upload_to_native_imagestore(sesh, endpoint, abspath, basename, show_progress, timeout)

    else:
        raise CLIError('Unsupported image store connection string. Value should be either '
                       '"fabric:ImageStore", or start with "file:"')

    # If code has reached here, it means that upload was successful
    # To reach here, user must have agreed to clear this folder or exist the API
    # So we can safely delete the contents
    # User is expected to not create a folder by the same name during the upload duration
    # If needed, we can consider adding our content under a GUID in the future
    if compress and not keep_compressed:
        # Remove the generated files
        if show_progress:
            print('Removing generated folder ' + created_dir_path)
        shutil.rmtree(created_dir_path)

def parse_app_params(formatted_params):
    """Parse application parameters from string"""
    from azure.servicefabric.models import ApplicationParameter

    if formatted_params is None:
        return None

    res = []
    for k in formatted_params:
        param = ApplicationParameter(key=k, value=formatted_params[k])
        res.append(param)

    return res

def parse_app_metrics(formatted_metrics):
    """Parse application metrics description from string"""
    from azure.servicefabric.models import ApplicationMetricDescription

    if formatted_metrics is None:
        return None

    res = []

    for metric in formatted_metrics:
        metric_name = metric.get('name', None)

        if not metric_name:
            raise CLIError('Could not find required application metric name')

        maximum_capacity = metric.get('maximum_capacity', None)
        reservation_capacity = metric.get('reservation_capacity', None)
        total_application_capacity = metric.get('total_application_capacity', None)

        res.append(ApplicationMetricDescription(
            name=metric_name,
            maximum_capacity=maximum_capacity,
            reservation_capacity=reservation_capacity,
            total_application_capacity=total_application_capacity))

    return res

def create(client,  # pylint: disable=too-many-locals,too-many-arguments
           app_name, app_type, app_version, parameters=None,
           min_node_count=0, max_node_count=0, metrics=None,
           timeout=60):
    """
    Creates a Service Fabric application using the specified description.
    :param str app_name: The name of the application, including the 'fabric:'
    URI scheme.
    :param str app_type: The application type name found in the application
    manifest.
    :param str app_version: The version of the application type as defined in
    the application manifest.
    :param str parameters: A JSON encoded list of application parameter
    overrides to be applied when creating the application.
    :param int min_node_count: The minimum number of nodes where Service
    Fabric will reserve capacity for this application. Note that this does not
    mean that the services of this application will be placed on all of those
    nodes.
    :param int max_node_count: The maximum number of nodes where Service
    Fabric will reserve capacity for this application. Note that this does not
    mean that the services of this application will be placed on all of those
    nodes.
    :param str metrics: A JSON encoded list of application capacity metric
    descriptions. A metric is defined as a name, associated with a set of
    capacities for each node that the application exists on.
    """
    from azure.servicefabric.models import  ApplicationDescription, ApplicationCapacityDescription

    if (any([min_node_count, max_node_count]) and
            not all([min_node_count, max_node_count])):
        raise CLIError('Must specify both maximum and minimum node count')

    if (all([min_node_count, max_node_count]) and
            min_node_count > max_node_count):
        raise CLIError('The minimum node reserve capacity count cannot '
                       'be greater than the maximum node count')

    app_params = parse_app_params(parameters)

    app_metrics = parse_app_metrics(metrics)

    app_cap_desc = ApplicationCapacityDescription(minimum_nodes=min_node_count,
                                                  maximum_nodes=max_node_count,
                                                  application_metrics=app_metrics)

    app_desc = ApplicationDescription(name=app_name,
                                      type_name=app_type,
                                      type_version=app_version,
                                      parameter_list=app_params,
                                      application_capacity=app_cap_desc)

    client.create_application(app_desc, timeout)

def upgrade(  # pylint: disable=too-many-arguments,too-many-locals,missing-docstring
        client, application_id, application_version, parameters,
        mode="UnmonitoredAuto", replica_set_check_timeout=None,
        force_restart=None, failure_action=None,
        health_check_wait_duration="0",
        health_check_stable_duration="PT0H2M0S",
        health_check_retry_timeout="PT0H10M0S",
        upgrade_timeout="P10675199DT02H48M05.4775807S",
        upgrade_domain_timeout="P10675199DT02H48M05.4775807S",
        warning_as_error=False,
        max_unhealthy_apps=0, default_service_health_policy=None,
        service_health_policy=None, timeout=60):
    from azure.servicefabric.models import (ApplicationUpgradeDescription,
                                            MonitoringPolicyDescription,
                                            ApplicationHealthPolicy)

    from sfctl.custom_health import (parse_service_health_policy_map,
                                     parse_service_health_policy)

    monitoring_policy = MonitoringPolicyDescription(
        failure_action=failure_action,
        health_check_wait_duration_in_milliseconds=health_check_wait_duration,
        health_check_stable_duration_in_milliseconds=health_check_stable_duration,
        health_check_retry_timeout_in_milliseconds=health_check_retry_timeout,
        upgrade_timeout_in_milliseconds=upgrade_timeout,
        upgrade_domain_timeout_in_milliseconds=upgrade_domain_timeout
    )

    # Must always have empty list
    app_params = parse_app_params(parameters)
    if app_params is None:
        app_params = []

    def_shp = parse_service_health_policy(default_service_health_policy)

    map_shp = parse_service_health_policy_map(service_health_policy)

    app_health_policy = ApplicationHealthPolicy(
        consider_warning_as_error=warning_as_error,
        max_percent_unhealthy_deployed_applications=max_unhealthy_apps,
        default_service_type_health_policy=def_shp,
        service_type_health_policy_map=map_shp)

    desc = ApplicationUpgradeDescription(
        name='fabric:/' + application_id,
        target_application_type_version=application_version,
        parameters=app_params,
        upgrade_kind='Rolling',
        rolling_upgrade_mode=mode,
        upgrade_replica_set_check_timeout_in_seconds=replica_set_check_timeout,
        force_restart=force_restart,
        monitoring_policy=monitoring_policy,
        application_health_policy=app_health_policy)

    client.start_application_upgrade(application_id, desc, timeout)

# SIG # Begin Windows Authenticode signature block
# MIIoKgYJKoZIhvcNAQcCoIIoGzCCKBcCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCAGMWHHK1jji6IF
# ObVe92G8ffWQmkbG70RS/rBDcCruIKCCDXYwggX0MIID3KADAgECAhMzAAADrzBA
# DkyjTQVBAAAAAAOvMA0GCSqGSIb3DQEBCwUAMH4xCzAJBgNVBAYTAlVTMRMwEQYD
# VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24xKDAmBgNVBAMTH01pY3Jvc29mdCBDb2RlIFNpZ25p
# bmcgUENBIDIwMTEwHhcNMjMxMTE2MTkwOTAwWhcNMjQxMTE0MTkwOTAwWjB0MQsw
# CQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9u
# ZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMR4wHAYDVQQDExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
# AQDOS8s1ra6f0YGtg0OhEaQa/t3Q+q1MEHhWJhqQVuO5amYXQpy8MDPNoJYk+FWA
# hePP5LxwcSge5aen+f5Q6WNPd6EDxGzotvVpNi5ve0H97S3F7C/axDfKxyNh21MG
# 0W8Sb0vxi/vorcLHOL9i+t2D6yvvDzLlEefUCbQV/zGCBjXGlYJcUj6RAzXyeNAN
# xSpKXAGd7Fh+ocGHPPphcD9LQTOJgG7Y7aYztHqBLJiQQ4eAgZNU4ac6+8LnEGAL
# go1ydC5BJEuJQjYKbNTy959HrKSu7LO3Ws0w8jw6pYdC1IMpdTkk2puTgY2PDNzB
# tLM4evG7FYer3WX+8t1UMYNTAgMBAAGjggFzMIIBbzAfBgNVHSUEGDAWBgorBgEE
# AYI3TAgBBggrBgEFBQcDAzAdBgNVHQ4EFgQURxxxNPIEPGSO8kqz+bgCAQWGXsEw
# RQYDVR0RBD4wPKQ6MDgxHjAcBgNVBAsTFU1pY3Jvc29mdCBDb3Jwb3JhdGlvbjEW
# MBQGA1UEBRMNMjMwMDEyKzUwMTgyNjAfBgNVHSMEGDAWgBRIbmTlUAXTgqoXNzci
# tW2oynUClTBUBgNVHR8ETTBLMEmgR6BFhkNodHRwOi8vd3d3Lm1pY3Jvc29mdC5j
# b20vcGtpb3BzL2NybC9NaWNDb2RTaWdQQ0EyMDExXzIwMTEtMDctMDguY3JsMGEG
# CCsGAQUFBwEBBFUwUzBRBggrBgEFBQcwAoZFaHR0cDovL3d3dy5taWNyb3NvZnQu
# Y29tL3BraW9wcy9jZXJ0cy9NaWNDb2RTaWdQQ0EyMDExXzIwMTEtMDctMDguY3J0
# MAwGA1UdEwEB/wQCMAAwDQYJKoZIhvcNAQELBQADggIBAISxFt/zR2frTFPB45Yd
# mhZpB2nNJoOoi+qlgcTlnO4QwlYN1w/vYwbDy/oFJolD5r6FMJd0RGcgEM8q9TgQ
# 2OC7gQEmhweVJ7yuKJlQBH7P7Pg5RiqgV3cSonJ+OM4kFHbP3gPLiyzssSQdRuPY
# 1mIWoGg9i7Y4ZC8ST7WhpSyc0pns2XsUe1XsIjaUcGu7zd7gg97eCUiLRdVklPmp
# XobH9CEAWakRUGNICYN2AgjhRTC4j3KJfqMkU04R6Toyh4/Toswm1uoDcGr5laYn
# TfcX3u5WnJqJLhuPe8Uj9kGAOcyo0O1mNwDa+LhFEzB6CB32+wfJMumfr6degvLT
# e8x55urQLeTjimBQgS49BSUkhFN7ois3cZyNpnrMca5AZaC7pLI72vuqSsSlLalG
# OcZmPHZGYJqZ0BacN274OZ80Q8B11iNokns9Od348bMb5Z4fihxaBWebl8kWEi2O
# PvQImOAeq3nt7UWJBzJYLAGEpfasaA3ZQgIcEXdD+uwo6ymMzDY6UamFOfYqYWXk
# ntxDGu7ngD2ugKUuccYKJJRiiz+LAUcj90BVcSHRLQop9N8zoALr/1sJuwPrVAtx
# HNEgSW+AKBqIxYWM4Ev32l6agSUAezLMbq5f3d8x9qzT031jMDT+sUAoCw0M5wVt
# CUQcqINPuYjbS1WgJyZIiEkBMIIHejCCBWKgAwIBAgIKYQ6Q0gAAAAAAAzANBgkq
# hkiG9w0BAQsFADCBiDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldhc2hpbmd0b24x
# EDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBDb3Jwb3JhdGlv
# bjEyMDAGA1UEAxMpTWljcm9zb2Z0IFJvb3QgQ2VydGlmaWNhdGUgQXV0aG9yaXR5
# IDIwMTEwHhcNMTEwNzA4MjA1OTA5WhcNMjYwNzA4MjEwOTA5WjB+MQswCQYDVQQG
# EwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwG
# A1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSgwJgYDVQQDEx9NaWNyb3NvZnQg
# Q29kZSBTaWduaW5nIFBDQSAyMDExMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIIC
# CgKCAgEAq/D6chAcLq3YbqqCEE00uvK2WCGfQhsqa+laUKq4BjgaBEm6f8MMHt03
# a8YS2AvwOMKZBrDIOdUBFDFC04kNeWSHfpRgJGyvnkmc6Whe0t+bU7IKLMOv2akr
# rnoJr9eWWcpgGgXpZnboMlImEi/nqwhQz7NEt13YxC4Ddato88tt8zpcoRb0Rrrg
# OGSsbmQ1eKagYw8t00CT+OPeBw3VXHmlSSnnDb6gE3e+lD3v++MrWhAfTVYoonpy
# 4BI6t0le2O3tQ5GD2Xuye4Yb2T6xjF3oiU+EGvKhL1nkkDstrjNYxbc+/jLTswM9
# sbKvkjh+0p2ALPVOVpEhNSXDOW5kf1O6nA+tGSOEy/S6A4aN91/w0FK/jJSHvMAh
# dCVfGCi2zCcoOCWYOUo2z3yxkq4cI6epZuxhH2rhKEmdX4jiJV3TIUs+UsS1Vz8k
# A/DRelsv1SPjcF0PUUZ3s/gA4bysAoJf28AVs70b1FVL5zmhD+kjSbwYuER8ReTB
# w3J64HLnJN+/RpnF78IcV9uDjexNSTCnq47f7Fufr/zdsGbiwZeBe+3W7UvnSSmn
# Eyimp31ngOaKYnhfsi+E11ecXL93KCjx7W3DKI8sj0A3T8HhhUSJxAlMxdSlQy90
# lfdu+HggWCwTXWCVmj5PM4TasIgX3p5O9JawvEagbJjS4NaIjAsCAwEAAaOCAe0w
# ggHpMBAGCSsGAQQBgjcVAQQDAgEAMB0GA1UdDgQWBBRIbmTlUAXTgqoXNzcitW2o
# ynUClTAZBgkrBgEEAYI3FAIEDB4KAFMAdQBiAEMAQTALBgNVHQ8EBAMCAYYwDwYD
# VR0TAQH/BAUwAwEB/zAfBgNVHSMEGDAWgBRyLToCMZBDuRQFTuHqp8cx0SOJNDBa
# BgNVHR8EUzBRME+gTaBLhklodHRwOi8vY3JsLm1pY3Jvc29mdC5jb20vcGtpL2Ny
# bC9wcm9kdWN0cy9NaWNSb29DZXJBdXQyMDExXzIwMTFfMDNfMjIuY3JsMF4GCCsG
# AQUFBwEBBFIwUDBOBggrBgEFBQcwAoZCaHR0cDovL3d3dy5taWNyb3NvZnQuY29t
# L3BraS9jZXJ0cy9NaWNSb29DZXJBdXQyMDExXzIwMTFfMDNfMjIuY3J0MIGfBgNV
# HSAEgZcwgZQwgZEGCSsGAQQBgjcuAzCBgzA/BggrBgEFBQcCARYzaHR0cDovL3d3
# dy5taWNyb3NvZnQuY29tL3BraW9wcy9kb2NzL3ByaW1hcnljcHMuaHRtMEAGCCsG
# AQUFBwICMDQeMiAdAEwAZQBnAGEAbABfAHAAbwBsAGkAYwB5AF8AcwB0AGEAdABl
# AG0AZQBuAHQALiAdMA0GCSqGSIb3DQEBCwUAA4ICAQBn8oalmOBUeRou09h0ZyKb
# C5YR4WOSmUKWfdJ5DJDBZV8uLD74w3LRbYP+vj/oCso7v0epo/Np22O/IjWll11l
# hJB9i0ZQVdgMknzSGksc8zxCi1LQsP1r4z4HLimb5j0bpdS1HXeUOeLpZMlEPXh6
# I/MTfaaQdION9MsmAkYqwooQu6SpBQyb7Wj6aC6VoCo/KmtYSWMfCWluWpiW5IP0
# wI/zRive/DvQvTXvbiWu5a8n7dDd8w6vmSiXmE0OPQvyCInWH8MyGOLwxS3OW560
# STkKxgrCxq2u5bLZ2xWIUUVYODJxJxp/sfQn+N4sOiBpmLJZiWhub6e3dMNABQam
# ASooPoI/E01mC8CzTfXhj38cbxV9Rad25UAqZaPDXVJihsMdYzaXht/a8/jyFqGa
# J+HNpZfQ7l1jQeNbB5yHPgZ3BtEGsXUfFL5hYbXw3MYbBL7fQccOKO7eZS/sl/ah
# XJbYANahRr1Z85elCUtIEJmAH9AAKcWxm6U/RXceNcbSoqKfenoi+kiVH6v7RyOA
# 9Z74v2u3S5fi63V4GuzqN5l5GEv/1rMjaHXmr/r8i+sLgOppO6/8MO0ETI7f33Vt
# Y5E90Z1WTk+/gFcioXgRMiF670EKsT/7qMykXcGhiJtXcVZOSEXAQsmbdlsKgEhr
# /Xmfwb1tbWrJUnMTDXpQzTGCGgowghoGAgEBMIGVMH4xCzAJBgNVBAYTAlVTMRMw
# EQYDVQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVN
# aWNyb3NvZnQgQ29ycG9yYXRpb24xKDAmBgNVBAMTH01pY3Jvc29mdCBDb2RlIFNp
# Z25pbmcgUENBIDIwMTECEzMAAAOvMEAOTKNNBUEAAAAAA68wDQYJYIZIAWUDBAIB
# BQCgga4wGQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYKKwYBBAGCNwIBCzEO
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIAEjk5+9pJ3by89BgjAqB92l
# PnD3OoUQYHJ1Rnodre/yMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEAx3t9/9GKVcme97lY6UB9a9/pdiemC06/wCSuqjIDxT3N+4+5npFCQiva
# uNtEptdLhEXWniAmEdpy2UiRbtrVxJeAicryxMixytt3v9MTghly7bAZabBT9QoG
# SDeiRX0LnuPxFDAfkRPglcjg7IQHc/yoxM32fQXFiQvD3gcii33B2Ze4Q+bJnSSW
# Oh0rPSdE25WRnQw5fMyZ8gIwrbYrYkP9J3q6zoOrXg9ub2oe1zp+fI7yO5Jq1ML0
# LXTZbnjAQGTq87rO8qjynPIqG/0TorN0SehtHmOxV1dttTARXq8cefD6G70mxPJ3
# 9RhPtMks1EnzxpTWEzYTXSD0vbk3vKGCF5QwgheQBgorBgEEAYI3AwMBMYIXgDCC
# F3wGCSqGSIb3DQEHAqCCF20wghdpAgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFSBgsq
# hkiG9w0BCRABBKCCAUEEggE9MIIBOQIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCD9Rif2mARVehF8jTLM5JrevYOKn2ik/rd+XitxC131GQIGZmrZP52o
# GBMyMDI0MDYyMDE1MDAwMS40MDdaMASAAgH0oIHRpIHOMIHLMQswCQYDVQQGEwJV
# UzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UE
# ChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1l
# cmljYSBPcGVyYXRpb25zMScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046QTQwMC0w
# NUUwLUQ5NDcxJTAjBgNVBAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2Wg
# ghHqMIIHIDCCBQigAwIBAgITMwAAAezgK6SC0JFSgAABAAAB7DANBgkqhkiG9w0B
# AQsFADB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UE
# BxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYD
# VQQDEx1NaWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMDAeFw0yMzEyMDYxODQ1
# MzhaFw0yNTAzMDUxODQ1MzhaMIHLMQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2Fz
# aGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENv
# cnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1lcmljYSBPcGVyYXRpb25z
# MScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046QTQwMC0wNUUwLUQ5NDcxJTAjBgNV
# BAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2UwggIiMA0GCSqGSIb3DQEB
# AQUAA4ICDwAwggIKAoICAQCwR/RuCTbgxUWVm/Vdul22uwdEZm0IoAFs6oIr39VK
# /ItP80cn+8TmtP67iabB4DmAKJ9GH6dJGhEPJpY4vTKRSOwrRNxVIKoPPeUF3f4V
# yHEco/u1QUadlwD132NuZCxbnh6Mi2lLG7pDvszZqMG7S3MCi2bk2nvtGKdeAIL+
# H77gL4r01TSWb7rsE2Jb1P/N6Y/W1CqDi1/Ib3/zRqWXt4zxvdIGcPjS4ZKyQEF3
# SEZAq4XIjiyowPHaqNbZxdf2kWO/ajdfTU85t934CXAinb0o+uQ9KtaKNLVVcNf5
# QpS4f6/MsXOvIFuCYMRdKDjpmvowAeL+1j27bCxCBpDQHrWkfPzZp/X+bt9C7E5h
# PP6HVRoqBYR7u1gUf5GEq+5r1HA0jajn0Q6OvfYckE0HdOv6KWa+sAmJG7PDvTZa
# e77homzx6IPqggVpNZuCk79SfVmnKu9F58UAnU58TqDHEzGsQnMUQKstS3zjn6SU
# 0NLEFNCetluaKkqWDRVLEWbu329IEh3tqXPXfy6Rh/wCbwe9SCJIoqtBexBrPyQY
# A2Xaz1fK9ysTsx0kA9V1JwVV44Ia9c+MwtAR6sqKdAgRo/bs/Xu8gua8LDe6KWyu
# 974e9mGW7ZO8narDFrAT1EXGHDueygSKvv2K7wB8lAgMGJj73CQvr+jqoWwx6Xdy
# eQIDAQABo4IBSTCCAUUwHQYDVR0OBBYEFPRa0Edk/iv1whYQsV8UgEf4TIWGMB8G
# A1UdIwQYMBaAFJ+nFV0AXmJdg/Tl0mWnG1M1GelyMF8GA1UdHwRYMFYwVKBSoFCG
# Tmh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY3JsL01pY3Jvc29mdCUy
# MFRpbWUtU3RhbXAlMjBQQ0ElMjAyMDEwKDEpLmNybDBsBggrBgEFBQcBAQRgMF4w
# XAYIKwYBBQUHMAKGUGh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY2Vy
# dHMvTWljcm9zb2Z0JTIwVGltZS1TdGFtcCUyMFBDQSUyMDIwMTAoMSkuY3J0MAwG
# A1UdEwEB/wQCMAAwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwDgYDVR0PAQH/BAQD
# AgeAMA0GCSqGSIb3DQEBCwUAA4ICAQCSvMSkMSrvjlDPag8ARb0OFrAQtSLMDpN0
# UY3FjvPhwGKDrrixmnuMfjrmVjRq1u8IhkDvGF/bffbFTr+IAnDSeg8TB9zfG/4y
# bknuopklbeGjbt7MLxpfholCERyEc20PMZKJz9SvzfuO1n5xrrLOL8m0nmv5kBcv
# +y1AXJ5QcLicmhe2Ip3/D67Ed6oPqQI03mDjYaS1NQhBNtu57wPKXZ1EoNToBk8b
# A6839w119b+a9WToqIskdRGoP5xjDIv+mc0vBHhZGkJVvfIhm4Ap8zptC7xVAly0
# jeOv5dUGMCYgZjvoTmgd45bqAwundmPlGur7eleWYedLQf7s3L5+qfaY/xEh/9uo
# 17SnM/gHVSGAzvnreGhOrB2LtdKoVSe5LbYpihXctDe76iYtL+mhxXPEpzda3bJl
# hPTOQ3KOEZApVERBo5yltWjPCWlXxyCpl5jj9nY0nfd071bemnou8A3rUZrdgKIa
# utsH7SHOiOebZGqNu+622vJta3eAYsCAaxAcB9BiJPla7Xad9qrTYdT45VlCYTtB
# SY4oVRsedSADv99jv/iYIAGy1bCytua0o/Qqv9erKmzQCTVMXaDc25DTLcMGJrRu
# a3K0xivdtnoBexzVJr6yXqM+Ba2whIVRvGcriBkKX0FJFeW7r29XX+k0e4DnG6iB
# HKQjec6VNzCCB3EwggVZoAMCAQICEzMAAAAVxedrngKbSZkAAAAAABUwDQYJKoZI
# hvcNAQELBQAwgYgxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpXYXNoaW5ndG9uMRAw
# DgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNyb3NvZnQgQ29ycG9yYXRpb24x
# MjAwBgNVBAMTKU1pY3Jvc29mdCBSb290IENlcnRpZmljYXRlIEF1dGhvcml0eSAy
# MDEwMB4XDTIxMDkzMDE4MjIyNVoXDTMwMDkzMDE4MzIyNVowfDELMAkGA1UEBhMC
# VVMxEzARBgNVBAgTCldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNV
# BAoTFU1pY3Jvc29mdCBDb3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRp
# bWUtU3RhbXAgUENBIDIwMTAwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoIC
# AQDk4aZM57RyIQt5osvXJHm9DtWC0/3unAcH0qlsTnXIyjVX9gF/bErg4r25Phdg
# M/9cT8dm95VTcVrifkpa/rg2Z4VGIwy1jRPPdzLAEBjoYH1qUoNEt6aORmsHFPPF
# dvWGUNzBRMhxXFExN6AKOG6N7dcP2CZTfDlhAnrEqv1yaa8dq6z2Nr41JmTamDu6
# GnszrYBbfowQHJ1S/rboYiXcag/PXfT+jlPP1uyFVk3v3byNpOORj7I5LFGc6XBp
# Dco2LXCOMcg1KL3jtIckw+DJj361VI/c+gVVmG1oO5pGve2krnopN6zL64NF50Zu
# yjLVwIYwXE8s4mKyzbnijYjklqwBSru+cakXW2dg3viSkR4dPf0gz3N9QZpGdc3E
# XzTdEonW/aUgfX782Z5F37ZyL9t9X4C626p+Nuw2TPYrbqgSUei/BQOj0XOmTTd0
# lBw0gg/wEPK3Rxjtp+iZfD9M269ewvPV2HM9Q07BMzlMjgK8QmguEOqEUUbi0b1q
# GFphAXPKZ6Je1yh2AuIzGHLXpyDwwvoSCtdjbwzJNmSLW6CmgyFdXzB0kZSU2LlQ
# +QuJYfM2BjUYhEfb3BvR/bLUHMVr9lxSUV0S2yW6r1AFemzFER1y7435UsSFF5PA
# PBXbGjfHCBUYP3irRbb1Hode2o+eFnJpxq57t7c+auIurQIDAQABo4IB3TCCAdkw
# EgYJKwYBBAGCNxUBBAUCAwEAATAjBgkrBgEEAYI3FQIEFgQUKqdS/mTEmr6CkTxG
# NSnPEP8vBO4wHQYDVR0OBBYEFJ+nFV0AXmJdg/Tl0mWnG1M1GelyMFwGA1UdIARV
# MFMwUQYMKwYBBAGCN0yDfQEBMEEwPwYIKwYBBQUHAgEWM2h0dHA6Ly93d3cubWlj
# cm9zb2Z0LmNvbS9wa2lvcHMvRG9jcy9SZXBvc2l0b3J5Lmh0bTATBgNVHSUEDDAK
# BggrBgEFBQcDCDAZBgkrBgEEAYI3FAIEDB4KAFMAdQBiAEMAQTALBgNVHQ8EBAMC
# AYYwDwYDVR0TAQH/BAUwAwEB/zAfBgNVHSMEGDAWgBTV9lbLj+iiXGJo0T2UkFvX
# zpoYxDBWBgNVHR8ETzBNMEugSaBHhkVodHRwOi8vY3JsLm1pY3Jvc29mdC5jb20v
# cGtpL2NybC9wcm9kdWN0cy9NaWNSb29DZXJBdXRfMjAxMC0wNi0yMy5jcmwwWgYI
# KwYBBQUHAQEETjBMMEoGCCsGAQUFBzAChj5odHRwOi8vd3d3Lm1pY3Jvc29mdC5j
# b20vcGtpL2NlcnRzL01pY1Jvb0NlckF1dF8yMDEwLTA2LTIzLmNydDANBgkqhkiG
# 9w0BAQsFAAOCAgEAnVV9/Cqt4SwfZwExJFvhnnJL/Klv6lwUtj5OR2R4sQaTlz0x
# M7U518JxNj/aZGx80HU5bbsPMeTCj/ts0aGUGCLu6WZnOlNN3Zi6th542DYunKmC
# VgADsAW+iehp4LoJ7nvfam++Kctu2D9IdQHZGN5tggz1bSNU5HhTdSRXud2f8449
# xvNo32X2pFaq95W2KFUn0CS9QKC/GbYSEhFdPSfgQJY4rPf5KYnDvBewVIVCs/wM
# nosZiefwC2qBwoEZQhlSdYo2wh3DYXMuLGt7bj8sCXgU6ZGyqVvfSaN0DLzskYDS
# PeZKPmY7T7uG+jIa2Zb0j/aRAfbOxnT99kxybxCrdTDFNLB62FD+CljdQDzHVG2d
# Y3RILLFORy3BFARxv2T5JL5zbcqOCb2zAVdJVGTZc9d/HltEAY5aGZFrDZ+kKNxn
# GSgkujhLmm77IVRrakURR6nxt67I6IleT53S0Ex2tVdUCbFpAUR+fKFhbHP+Crvs
# QWY9af3LwUFJfn6Tvsv4O+S3Fb+0zj6lMVGEvL8CwYKiexcdFYmNcP7ntdAoGokL
# jzbaukz5m/8K6TT4JDVnK+ANuOaMmdbhIurwJ0I9JZTmdHRbatGePu1+oDEzfbzL
# 6Xu/OHBE0ZDxyKs6ijoIYn/ZcGNTTY3ugm2lBRDBcQZqELQdVTNYs6FwZvKhggNN
# MIICNQIBATCB+aGB0aSBzjCByzELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldhc2hp
# bmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBDb3Jw
# b3JhdGlvbjElMCMGA1UECxMcTWljcm9zb2Z0IEFtZXJpY2EgT3BlcmF0aW9uczEn
# MCUGA1UECxMeblNoaWVsZCBUU1MgRVNOOkE0MDAtMDVFMC1EOTQ3MSUwIwYDVQQD
# ExxNaWNyb3NvZnQgVGltZS1TdGFtcCBTZXJ2aWNloiMKAQEwBwYFKw4DAhoDFQCO
# HPtgVdz9EW0iPNL/BXqJoqVMf6CBgzCBgKR+MHwxCzAJBgNVBAYTAlVTMRMwEQYD
# VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24xJjAkBgNVBAMTHU1pY3Jvc29mdCBUaW1lLVN0YW1w
# IFBDQSAyMDEwMA0GCSqGSIb3DQEBCwUAAgUA6h6RkDAiGA8yMDI0MDYyMDExMzEy
# OFoYDzIwMjQwNjIxMTEzMTI4WjB0MDoGCisGAQQBhFkKBAExLDAqMAoCBQDqHpGQ
# AgEAMAcCAQACAggGMAcCAQACAhNsMAoCBQDqH+MQAgEAMDYGCisGAQQBhFkKBAIx
# KDAmMAwGCisGAQQBhFkKAwKgCjAIAgEAAgMHoSChCjAIAgEAAgMBhqAwDQYJKoZI
# hvcNAQELBQADggEBADEUnqpOO4ssnLP9MW3rdZWF8MtyBLv8vAj4EN4wDNT3S+eM
# jq+TbfGYqz/91mOuQYAqtUxW2z5FzTK7oGLUlqLBTf4kaOjQ3bIbej7CspO8WhDG
# vCFnqWmTjx9909/nMuvAsNRUdl15PPsL9g4/koQrbWPSip4cQ1rhpnxEo7kkP4YP
# tV0GVlAxKmkgsmakeNH8d8caZxTmYxB7fKQdlRq52fwnkxwTd/XjjhlNiJn+9o5s
# /HrYaJx4G/fUc9zbT/23waOqkJBF4Mga06lSPMKCow7qxXbXsq+kXyzg5Onk2+eu
# WppA+xQVQzMCd/gLBJd3VDkCaux84EikAdYdYZ4xggQNMIIECQIBATCBkzB8MQsw
# CQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9u
# ZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYDVQQDEx1NaWNy
# b3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMAITMwAAAezgK6SC0JFSgAABAAAB7DAN
# BglghkgBZQMEAgEFAKCCAUowGgYJKoZIhvcNAQkDMQ0GCyqGSIb3DQEJEAEEMC8G
# CSqGSIb3DQEJBDEiBCAyQlsJn6cLebOOIKhpxAr6oh2cP4/nnP9jUq4nbhEzZjCB
# +gYLKoZIhvcNAQkQAi8xgeowgecwgeQwgb0EICcJ5vVqfTfIhx21QBBbKyo/xciQ
# IXaoMWULejAE1QqDMIGYMIGApH4wfDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldh
# c2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBD
# b3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENBIDIw
# MTACEzMAAAHs4CukgtCRUoAAAQAAAewwIgQgJfj+/uHgptLFvuzTKH4AJJaJUS86
# 8THuToorLBW/tyQwDQYJKoZIhvcNAQELBQAEggIAdlG1hbCuxsdQh8PtDV33youT
# ZpIo1UB3RrtJlcPhV2ACwhWOR7UvFr63VOy6qPEH4XUSDgeBiyOV2wDs6kKdiBIx
# oPkGAIb5FkC3XqmgjHSjkOffeWoxbHAIju/4RGWshBcbWzwQAXIuODhDRSTVmH2c
# HwVRgqgzp1/mKHNzkcooV8RhnKED1eAdta6sPJ3NtUuYCFphkN+9wFhHouvxsIb7
# 7gfR8nkgMUJdWd+zgC0Zc4tuoQuWUy05f5oXXPaGKsjhGdwbp2PAHwYe6LKH7OxH
# w2HhICzRM4TNiU/SpXCSjaAC50vFXcvcj07b19SY2CVSX6Dmo5EQaMR1PQoXmh/P
# RBRqcpEXPy+3DBzW3M2oZSWlwzzCVB/ex9lCfFVNfaumd9K0d+Tg1FClv7mtIB9H
# VHiwhCHhieXpscoiCz0Tu9+hTTzfGFA4JSjB7xnCluHTRtdxGm9n2o0s29+4dsWh
# 7bgW12pq2LJzPjq8ylUfQ0gWsP5OB3QHiSsUKT0k/FhQ6doeyR4bSs43Jd1m+z0z
# xExC/vSPMxcn27IgQU3S/2kwbRDNzxfoel0O8oJXVm6zUTdfdtjn39apzGfW9WCO
# Ii8xE6qvY6vFlLdaBsGzmT7xrecOStubNhiDDnz6F6+OkEpgTfbZG4GTXCNagssf
# JmDEoqmpEEspLSInqwI=
# SIG # End Windows Authenticode signature block