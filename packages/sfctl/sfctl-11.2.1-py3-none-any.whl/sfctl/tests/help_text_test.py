# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Tests that -h does not return error and has all required text.
This only tests for commands/subgroups which are specified in this file.
This does not test the correctness of help text content."""

from __future__ import print_function
import unittest
from subprocess import Popen, PIPE


class HelpTextTests(unittest.TestCase):
    """Tests that -h does not return error and includes all help text."""

    def _validate_output_read_line(self,  # pylint: disable=too-many-arguments
                                   command_input, line,
                                   section, subgroups, commands,
                                   subgroups_index, commands_index):
        """ Read a line of text and validates it for correctness.
        Parameter line (string) should be unprocessed. For example, the line should not be
        stripped of starting or trailing white spaces.

        This method returns the updated values of subgroups_index and commands_index as a tuple.
        Tuple has ordering (subgroups_index, commands_index).
        If an error occurs during validation, an assert is called. """

        line = line.strip()

        if section in ('Command', 'Group'):
            # if the line starts with the inputted command, then it describes the command.
            # make sure the line has text after it
            if line.startswith(command_input):
                self.assertGreater(
                    len(line),
                    len(command_input),
                    msg='Validating help output failed on line: ' + line)

            return subgroups_index, commands_index

        if section == 'Arguments':
            # For lines that start with '--' (for argument descriptions), make sure that
            # there is something after the argument declaration
            if line.startswith('--'):
                self.assertIn(': ', line,
                              msg='Validating help output failed on line: ' + line)

                # Find the first ':' character and check that there are characters following it
                first_index = line.find(': ')
                self.assertGreater(
                    len(line),
                    first_index + 1,
                    msg='Validating help output failed on line: ' + line)

            return subgroups_index, commands_index

        if section in ('Commands', 'Subgroups'):
            # Make sure that if the line starts with the command/group in
            # the expected tuple, that a description follows it.
            # The line will either start with the name provided in the expected tuple,
            # or it will be a continuation line. Ignore continuation lines.
            first_word_of_line = line.split()[0].rstrip(':')

            if section == 'Commands':

                # If we've reached the end of the commands tuple, then skip, since everything
                # after this is a continuation line.
                if len(commands) == commands_index:
                    return subgroups_index, commands_index

                self.assertGreater(len(commands), commands_index,
                                   msg='None or missing expected commands provided in test for ' + command_input)  # pylint: disable=line-too-long
                if first_word_of_line == commands[commands_index]:
                    # make sure there is descriptive text in this line by checking
                    # that the line is longer than just the command.
                    self.assertGreater(
                        len(line),
                        len(first_word_of_line),
                        msg='Validating help text failed in "Commands" on line: ' + line)

                    commands_index += 1

            elif section == 'Subgroups':

                # If we've reached the end of the commands tuple, then skip
                if len(subgroups) == subgroups_index:
                    return subgroups_index, commands_index

                self.assertGreater(len(subgroups), subgroups_index,
                                   msg='None or missing expected subgroups provided in test for ' + command_input)  # pylint: disable=line-too-long
                if first_word_of_line == subgroups[subgroups_index]:
                    # make sure there is descriptive text in this line
                    self.assertGreater(
                        len(line),
                        len(first_word_of_line),
                        msg='Validating help text failed in "Subgroups" on line: ' + line)

                    subgroups_index += 1

            return subgroups_index, commands_index

        self.fail('Section name {0} is not supported'.format(section))
        # The following line will be reached. It is added so pylint does not complain
        # about inconsistent-return-statements.
        return subgroups_index, commands_index

    @classmethod
    def _validate_output_read_section_name(cls, line):
        """ Read a given line and validate it for correctness based on the given section.
        Parameter line (string) should be unprocessed. For example, the line should not be
        stripped of starting or trailing white spaces.

        Returns the section name if the given line designates the beginning of a new section.
        Returns None if the line does not. """

        if line.strip() and not line[0].isspace():
            # Use these lines to set the 'section' variable and move on to the next line
            line = line.strip().rstrip(':')
            if line == 'Commands':
                return 'Commands'
            if line in ('Arguments', 'Global Arguments'):
                return 'Arguments'
            if line == 'Group':
                return 'Group'
            if line == 'Subgroups':
                return 'Subgroups'
            if line == 'Command':
                return 'Command'

        return None

    def validate_output(self, command_input, subgroups=(), commands=()):  # pylint: disable=too-many-locals
        """
        This function verifies that the returned help text is correct, and that no exceptions
        are thrown during invocation. If commands are provided, this function will call itself
        recursively to verify the correctness of the commands. It verifies correctness by:

        - All listed subgroups and commands appear in alphabetical order. We do not check for the
            existence of extra subgroups and commands.
        - If subgroups or commands are not provided, then we expect it not to appear in
            the help text. If it does, there will be an assertion raised in this test.
        - All listed groups/subgroups, commands, and arguments have descriptive text

        Limitations: This test doesn't search for new commands which are added.
                     If a test entry is not added here, then that entry will not be
                     verified.

                     The first word of the line should not match a command name

        command_input (string): This represents the command for which you want to get the help text.
            For example, "sfctl" or "sfctl application" or "sfctl application list".
            Parameter command_input should not include the "-h" to get the help text, as this
            method will take care of that.

        subgroups (tuple of strings): This represents all of the subgroups expected in the
            help text. This tuple must be in alphabetical order.

        commands (tuple of strings): This represents all of the commands expected in the
            help text. This tuple must be in alphabetical order.

        Help text has two formats. One for groups, and one for commands.
        """

        help_command = command_input + ' -h'

        err = None
        returned_string = None

        try:
            # This variable tracks what sections of the help text we are in
            # Possibilities are Group, Subgroups, Commands, Command, Arguments,
            # and Global Arguments.
            # Once we no longer support python 2, change section options of enums
            section = 'Start'

            # A tracker to know how many subgroups or commands have appeared in help text so far
            # We use this to make sure that all expected items are returned
            subgroups_index = 0
            commands_index = 0

            # Call the provided command in command line
            # Do not split the help_command, as that breaks behavior:
            # Linux ignores the splits and takes only the first.

            pipe = Popen(help_command, shell=True, stdout=PIPE, stderr=PIPE)
            # returned_string and err are returned as bytes
            (returned_string, err) = pipe.communicate()

            if err:
                err = err.decode('utf-8')
                self.assertEqual(b'', err, msg='ERROR: in command: ' + help_command)

            if not returned_string:
                self.fail('No help text in command: ' + help_command)

            returned_string = returned_string.decode('utf-8')
            lines = returned_string.splitlines()

            for line in lines:

                if not line.strip():
                    continue

                # Check if we want to mark the start of a new section
                # Check this by seeing if the line is a top level description, ie: 'Commands:'
                # These are characterized by a new line with text starting without white space.
                read_section_output = self._validate_output_read_section_name(line)
                if read_section_output is not None:
                    section = read_section_output

                    # If this line is a section start, no additional processing
                    # is required. Move on to the next line.
                    continue

                # If this line is not a section start, then validate the correctness of the line.
                # This command returns a tuple which includes counters for subgroups and commands
                # which count how many instances of each have been processed.
                updated_indices = self._validate_output_read_line(command_input, line, section,
                                                                  subgroups, commands,
                                                                  subgroups_index,
                                                                  commands_index)
                subgroups_index = updated_indices[0]
                commands_index = updated_indices[1]

            # If section is still 'Start', the something has gone wrong.
            # It means that lines were not processed
            # correctly, since we expect some sections to appear.
            self.assertNotEqual(
                'Start',
                section,
                msg='Command {0}: incomplete help text: {1}'.format(help_command, returned_string))

            # Check that we have traversed completely through both
            # subgroups and commands
            self.assertEqual(len(commands), commands_index,
                             msg=('Not all commands listed in help text for '
                                  + help_command
                                  + '. \nThis may be a problem due incorrect expected ordering. '
                                    'I.e ("delete", "show", "list") != ("show", "delete", "list"). '
                                    '\nFirst diagnosis should be to run the help cmd yourself. \n'
                                    'If you passed in a single value to the tuple in validate '
                                    'output: commands=(set-telemetry,), like the example shown, '
                                    'you must pass in a comma after in the tuple, otherwise it '
                                    'will not be recognized as a tuple.'))
            self.assertEqual(len(subgroups), subgroups_index,
                             msg=('Not all subgroups listed in help text for '
                                  + help_command
                                  + '. This may be a problem due incorrect expected ordering. '
                                    'First diagnosis should be to run the help cmd yourself.'))

        except BaseException as exception:  # pylint: disable=broad-except
            if not err:
                self.fail(msg='ERROR: Command {0} returned error at execution. Output: {1} Error: {2}'.format(help_command, returned_string, str(exception)))  # pylint: disable=line-too-long
            else:
                self.fail(msg='ERROR: Command {0} returned error at execution. Output: {1} Error: {2}'.format(help_command, returned_string, err))  # pylint: disable=line-too-long

        # Once validation is done for the provided command_input,
        # if there are any commands returned in the help text, validate those commands.
        for command in commands:
            self.validate_output(command_input + ' ' + command)

    def test_help_documentation(self):
        """ Tests all help documentation to ensure that all commands have help text.
        This does not test for typos / correctness in the text itself.
        This test calls validate_output on all commands which sfctl has, without the
        '-h' flag included. The flag will be added by validate_ouput.

        Note: validate_output expects subgroups and commands in order. If out of alphabetical
        order, you will see an error for not all commands/subgroups being listed.

        Note: you do not need to call individual commands. Commands listed in the
        'commands' list will be called and verified automatically. You DO need
        an entry for each subgroup."""

        self.validate_output(
            'sfctl',
            subgroups=('application', 'chaos', 'cluster', 'compose', 'is', 'node',
                       'partition', 'property', 'replica', 'rpm', 'sa-cluster',
                       'service', 'settings', 'store'))

        self.validate_output(
            'sfctl chaos schedule',
            commands=('get', 'set'))

        self.validate_output(
            'sfctl settings telemetry',
            commands=('set-telemetry',))

        self.validate_output(
            'sfctl application',
            commands=('create', 'delete', 'deployed', 'deployed-health', 'deployed-list',
                      'health', 'info', 'list', 'load', 'manifest', 'provision',
                      'report-health', 'type', 'type-list', 'unprovision', 'upgrade',
                      'upgrade-resume', 'upgrade-rollback', 'upgrade-status', 'upload'))

        self.validate_output(
            'sfctl chaos',
            commands=('events', 'get', 'start', 'stop'))

        self.validate_output(
            'sfctl cluster',
            commands=('code-versions', 'config-versions', 'health', 'manifest',
                      'operation-cancel', 'operation-list', 'provision', 'recover-system',
                      'report-health', 'select', 'unprovision', 'upgrade', 'upgrade-resume',
                      'upgrade-rollback', 'upgrade-status', 'upgrade-update'))

        self.validate_output(
            'sfctl container',
            commands=('invoke-api', 'logs'))

        self.validate_output(
            'sfctl compose',
            commands=('create', 'list', 'remove', 'status', 'upgrade', 'upgrade-rollback',
                      'upgrade-status'))

        self.validate_output(
            'sfctl is',
            commands=('command', 'query'))

        self.validate_output(
            'sfctl node',
            commands=('add-configuration-parameter-overrides', 'add-node-tags', 'disable', 'enable',
                      'get-configuration-overrides', 'health', 'info', 'list', 'load',
                      'remove-configuration-overrides', 'remove-node-tags', 'remove-state', 'report-health',
                      'restart', 'transition', 'transition-status'))

        self.validate_output(
            'sfctl partition',
            commands=('data-loss', 'data-loss-status', 'get-loaded-partition-info-list',
                      'health', 'info', 'list', 'load', 'load-reset', 'move-instance', 'move-primary-replica',
                      'move-secondary-replica','quorum-loss', 'quorum-loss-status', 'recover', 'recover-all',
                       'report-health', 'restart', 'restart-status', 'svc-name'))

        self.validate_output(
            'sfctl property',
            commands=('delete', 'get', 'list', 'put'))

        self.validate_output(
            'sfctl replica',
            commands=('deployed', 'deployed-list', 'health', 'info', 'list', 'remove',
                      'report-health', 'restart'))

        self.validate_output(
            'sfctl rpm',
            commands=('approve-force', 'delete', 'list'))

        self.validate_output(
            'sfctl sa-cluster',
            commands=('config', 'config-upgrade', 'upgrade-status'))

        self.validate_output(
            'sfctl service',
            commands=('app-name', 'code-package-list', 'create', 'delete', 'deployed-type',
                      'deployed-type-list', 'description', 'get-container-logs',
                      'health', 'info', 'list', 'manifest', 'package-deploy',
                      'package-health', 'package-info', 'package-list', 'recover',
                      'report-health', 'resolve', 'type-list', 'update'))

        self.validate_output(
            'sfctl store',
            commands=('delete', 'root-info', 'stat'))

        self.validate_output(
            'sfctl events',
            commands=('all-applications-list', 'all-nodes-list', 'all-partitions-list',
                      'all-services-list', 'application-list', 'cluster-list', 'node-list',
                      'partition-all-replicas-list', 'partition-list', 'partition-replica-list',
                      'service-list'))
        
# SIG # Begin Windows Authenticode signature block
# MIIoLQYJKoZIhvcNAQcCoIIoHjCCKBoCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQse8BENmB6EqSR2hd
# JGAGggIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCAMnWNB1qV1FlNC
# BmnwWeOA62iN4U68RXWTI5bfTNYmQKCCDXYwggX0MIID3KADAgECAhMzAAADrzBA
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
# /Xmfwb1tbWrJUnMTDXpQzTGCGg0wghoJAgEBMIGVMH4xCzAJBgNVBAYTAlVTMRMw
# EQYDVQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVN
# aWNyb3NvZnQgQ29ycG9yYXRpb24xKDAmBgNVBAMTH01pY3Jvc29mdCBDb2RlIFNp
# Z25pbmcgUENBIDIwMTECEzMAAAOvMEAOTKNNBUEAAAAAA68wDQYJYIZIAWUDBAIB
# BQCgga4wGQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYKKwYBBAGCNwIBCzEO
# MAwGCisGAQQBgjcCARUwLwYJKoZIhvcNAQkEMSIEIOY6jrNEyr+uObV9O/mI3OyH
# ViFjxu8lXKcOyTfxkUChMEIGCisGAQQBgjcCAQwxNDAyoBSAEgBNAGkAYwByAG8A
# cwBvAGYAdKEagBhodHRwOi8vd3d3Lm1pY3Jvc29mdC5jb20wDQYJKoZIhvcNAQEB
# BQAEggEAmrVslT5ypidkxClVdv8JsynZQTwcxQqfpbtW9pfX3qkGuGTRjLki9m5p
# owLUIQ5rstcZR3hhj7HIXOhdP2TxD7/8tdmAceZWaDqxo21Cjg6hKEMfIepbrstN
# NgGrNTXB8sGYi+oieVgI/w6KOGWB02w6bU9lV+3gqwrze+J7a2wAVuj3IzsUhvJR
# d1kMA/pGkTc8o/nOzjcu93zN8i9Hp/GyNX5Obz+9hKlN3dQevzy5UWdaCif/+6bV
# HdjCfvWKup3XNJrag3ZqrVb711eLEkn4cBLGtzDA0cV0AJOtYHYd5aw9nix3WImF
# JemhPrk7qpml7Nv4BO6Rvxq3WJh5iKGCF5cwgheTBgorBgEEAYI3AwMBMYIXgzCC
# F38GCSqGSIb3DQEHAqCCF3AwghdsAgEDMQ8wDQYJYIZIAWUDBAIBBQAwggFSBgsq
# hkiG9w0BCRABBKCCAUEEggE9MIIBOQIBAQYKKwYBBAGEWQoDATAxMA0GCWCGSAFl
# AwQCAQUABCBxXGL8GINNKPFFvEcRuqkmRaFRnBxnzg5wDa12sdFfwQIGZmsCqZJ4
# GBMyMDI0MDYyMDE1MDAwMy45MzJaMASAAgH0oIHRpIHOMIHLMQswCQYDVQQGEwJV
# UzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UE
# ChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1l
# cmljYSBPcGVyYXRpb25zMScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046REMwMC0w
# NUUwLUQ5NDcxJTAjBgNVBAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2Wg
# ghHtMIIHIDCCBQigAwIBAgITMwAAAehQsIDPK3KZTQABAAAB6DANBgkqhkiG9w0B
# AQsFADB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UE
# BxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYD
# VQQDEx1NaWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMDAeFw0yMzEyMDYxODQ1
# MjJaFw0yNTAzMDUxODQ1MjJaMIHLMQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2Fz
# aGluZ3RvbjEQMA4GA1UEBxMHUmVkbW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENv
# cnBvcmF0aW9uMSUwIwYDVQQLExxNaWNyb3NvZnQgQW1lcmljYSBPcGVyYXRpb25z
# MScwJQYDVQQLEx5uU2hpZWxkIFRTUyBFU046REMwMC0wNUUwLUQ5NDcxJTAjBgNV
# BAMTHE1pY3Jvc29mdCBUaW1lLVN0YW1wIFNlcnZpY2UwggIiMA0GCSqGSIb3DQEB
# AQUAA4ICDwAwggIKAoICAQDhQXdE0WzXG7wzeC9SGdH6eVwdGlF6YgpU7weOFBkp
# W9yuEmJSDE1ADBx/0DTuRBaplSD8CR1QqyQmxRDD/CdvDyeZFAcZ6l2+nlMssmZy
# C8TPt1GTWAUt3GXUU6g0F0tIrFNLgofCjOvm3G0j482VutKS4wZT6bNVnBVsChr2
# AjmVbGDN/6Qs/EqakL5cwpGel1te7UO13dUwaPjOy0Wi1qYNmR8i7T1luj2JdFdf
# ZhMPyqyq/NDnZuONSbj8FM5xKBoar12ragC8/1CXaL1OMXBwGaRoJTYtksi9njuq
# 4wDkcAwitCZ5BtQ2NqPZ0lLiQB7O10Bm9zpHWn9x1/HmdAn4koMWKUDwH5sd/zDu
# 4vi887FWxm54kkWNvk8FeQ7ZZ0Q5gqGKW4g6revV2IdAxBobWdorqwvzqL70Wdsg
# DU/P5c0L8vYIskUJZedCGHM2hHIsNRyw9EFoSolDM+yCedkz69787s8nIp55icLf
# DoKw5hak5G6MWF6d71tcNzV9+v9RQKMa6Uwfyquredd5sqXWCXv++hek4A15WybI
# c6ufT0ilazKYZvDvoaswgjP0SeLW7mvmcw0FELzF1/uWaXElLHOXIlieKF2i/YzQ
# 6U50K9dbhnMaDcJSsG0hXLRTy/LQbsOD0hw7FuK0nmzotSx/5fo9g7fCzoFjk3tD
# EwIDAQABo4IBSTCCAUUwHQYDVR0OBBYEFPo5W8o980kMfRVQba6T34HwelLaMB8G
# A1UdIwQYMBaAFJ+nFV0AXmJdg/Tl0mWnG1M1GelyMF8GA1UdHwRYMFYwVKBSoFCG
# Tmh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY3JsL01pY3Jvc29mdCUy
# MFRpbWUtU3RhbXAlMjBQQ0ElMjAyMDEwKDEpLmNybDBsBggrBgEFBQcBAQRgMF4w
# XAYIKwYBBQUHMAKGUGh0dHA6Ly93d3cubWljcm9zb2Z0LmNvbS9wa2lvcHMvY2Vy
# dHMvTWljcm9zb2Z0JTIwVGltZS1TdGFtcCUyMFBDQSUyMDIwMTAoMSkuY3J0MAwG
# A1UdEwEB/wQCMAAwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwDgYDVR0PAQH/BAQD
# AgeAMA0GCSqGSIb3DQEBCwUAA4ICAQCWfcJm2rwXtPi74km6PKAkni9+BWotq+Qt
# DGgeT5F3ro7PsIUNKRkUytuGqI8thL3Jcrb03x6DOppYJEA+pb6o2qPjFddO1TLq
# vSXrYm+OgCLL+7+3FmRmfkRu8rHvprab0O19wDbukgO8I5Oi1RegMJl8t5k/UtE0
# Wb3zAlOHnCjLGSzP/Do3ptwhXokk02IvD7SZEBbPboGbtw4LCHsT2pFakpGOBh+I
# SUMXBf835CuVNfddwxmyGvNSzyEyEk5h1Vh7tpwP7z7rJ+HsiP4sdqBjj6Avopuf
# 4rxUAfrEbV6aj8twFs7WVHNiIgrHNna/55kyrAG9Yt19CPvkUwxYK0uZvPl2WC39
# nfc0jOTjivC7s/IUozE4tfy3JNkyQ1cNtvZftiX3j5Dt+eLOeuGDjvhJvYMIEkpk
# V68XLNH7+ZBfYa+PmfRYaoFFHCJKEoRSZ3PbDJPBiEhZ9yuxMddoMMQ19Tkyftot
# 6Ez0XhSmwjYBq39DvBFWhlyDGBhrU3GteDWiVd9YGSB2WnxuFMy5fbAK6o8PWz8Q
# RMiptXHK3HDBr2wWWEcrrgcTuHZIJTqepNoYlx9VRFvj/vCXaAFcmkW1nk7VE+ow
# aXr5RJjryDq9ubkyDq1mdrF/geaRALXcNZbfNXIkhXzXA6a8CiamcQW/DgmLJpiV
# QNriZYCHIDCCB3EwggVZoAMCAQICEzMAAAAVxedrngKbSZkAAAAAABUwDQYJKoZI
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
# 6Xu/OHBE0ZDxyKs6ijoIYn/ZcGNTTY3ugm2lBRDBcQZqELQdVTNYs6FwZvKhggNQ
# MIICOAIBATCB+aGB0aSBzjCByzELMAkGA1UEBhMCVVMxEzARBgNVBAgTCldhc2hp
# bmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29mdCBDb3Jw
# b3JhdGlvbjElMCMGA1UECxMcTWljcm9zb2Z0IEFtZXJpY2EgT3BlcmF0aW9uczEn
# MCUGA1UECxMeblNoaWVsZCBUU1MgRVNOOkRDMDAtMDVFMC1EOTQ3MSUwIwYDVQQD
# ExxNaWNyb3NvZnQgVGltZS1TdGFtcCBTZXJ2aWNloiMKAQEwBwYFKw4DAhoDFQCM
# JG4vg0juMOVn2BuKACUvP80FuqCBgzCBgKR+MHwxCzAJBgNVBAYTAlVTMRMwEQYD
# VQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVNaWNy
# b3NvZnQgQ29ycG9yYXRpb24xJjAkBgNVBAMTHU1pY3Jvc29mdCBUaW1lLVN0YW1w
# IFBDQSAyMDEwMA0GCSqGSIb3DQEBCwUAAgUA6h67CjAiGA8yMDI0MDYyMDE0Mjgy
# NloYDzIwMjQwNjIxMTQyODI2WjB3MD0GCisGAQQBhFkKBAExLzAtMAoCBQDqHrsK
# AgEAMAoCAQACAhjIAgH/MAcCAQACAhPOMAoCBQDqIAyKAgEAMDYGCisGAQQBhFkK
# BAIxKDAmMAwGCisGAQQBhFkKAwKgCjAIAgEAAgMHoSChCjAIAgEAAgMBhqAwDQYJ
# KoZIhvcNAQELBQADggEBADpTZoxYS1jzH7WPAp6pLakzjLo7Tla30KViT1bJTItI
# ei7uj9eE6XYDqt9VUqZnvTZylU6k1j7RGrXeWKP5von+O2F7sjQEQQoFncONu5I3
# trMhr/snK/TMula1uA+B5lh24WyUvvLvhV72DGmqrj7GYEf5kTAul7mR01TQ+0bs
# u/pHb1y3mQsxpkANlcAbNrVXA58J1oIqovj+NmVqiYuVKlBy6peixnBt163ToIfw
# U6KFjep8Zm41oDAAfPMbAYe9cgftu0uHKcjW1p5S70mkFCYHzCXbRXmzbGufibhP
# Jk4Pu4kyZaToCcVYoqu5NfxB3/a4hz8+wUIbjgRSW6ExggQNMIIECQIBATCBkzB8
# MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEQMA4GA1UEBxMHUmVk
# bW9uZDEeMBwGA1UEChMVTWljcm9zb2Z0IENvcnBvcmF0aW9uMSYwJAYDVQQDEx1N
# aWNyb3NvZnQgVGltZS1TdGFtcCBQQ0EgMjAxMAITMwAAAehQsIDPK3KZTQABAAAB
# 6DANBglghkgBZQMEAgEFAKCCAUowGgYJKoZIhvcNAQkDMQ0GCyqGSIb3DQEJEAEE
# MC8GCSqGSIb3DQEJBDEiBCCuLw7NztL6WVu6xgSagi3tv/QtDpBOzhR1H3q/xn8y
# uTCB+gYLKoZIhvcNAQkQAi8xgeowgecwgeQwgb0EICrS2sTVAoQggkHR59pNqige
# 0xfJT2J3U8W1Sc8H+OsdMIGYMIGApH4wfDELMAkGA1UEBhMCVVMxEzARBgNVBAgT
# Cldhc2hpbmd0b24xEDAOBgNVBAcTB1JlZG1vbmQxHjAcBgNVBAoTFU1pY3Jvc29m
# dCBDb3Jwb3JhdGlvbjEmMCQGA1UEAxMdTWljcm9zb2Z0IFRpbWUtU3RhbXAgUENB
# IDIwMTACEzMAAAHoULCAzytymU0AAQAAAegwIgQgS0S8r9Exog7fS7246n8tckMK
# I3TOE6S0MHQE5F8/5GIwDQYJKoZIhvcNAQELBQAEggIAoo5AoP0kIuezKs7zzbiZ
# rvAPAQLS6Hv2mde9li0VcDAOQdcLIotknXCHCM9UTo+yz7QlPDrvWXIx77UORiVX
# KjV8sPx4VxGquctBt3Cbv0Z4ZlT2OzI0dWB8GH+WjnGli3FE/EKGAfyZr3Wj66ef
# u93vSBgjZ2srgSrkeyn14BPLzsLO8ht/cj7yfc1UEhP5XXYMrbY7/oGcaNAjJNex
# KHZ4vuOFbmVfTO2EnI4admQVKRCiHxh9JKXE4+P/fUhjk8cDt4O3NISwjpKQPD9X
# OmlgS10bI4AyjiAlzZ7ut5KkFr4LRzem1qc3h7rDWpqYCpuALpc3Wlg98y5zBl/R
# IxQgHcNamAevOGNITv5RLhjU0wbChOaJ2FHRqeUADRHoNcGonNDnlX6ta1yaAHXL
# 1O7CkSq35Uc0lAIWgzHbqMHoeOotEHPe2pMfLe+RHPzBSur33XJMtbx72zL+8DJ6
# inc+hB8CTWRljr+nN8cyRYUiVWl1l6THASfyN5y8bikv2fwkqzsPufbz+bZ373gz
# +2YN7Vli/bgPjpZ5c4g74k+t9E9GueeI2oubeCxq4eaAeQOytpWX15qdaXD4UgeO
# wQRJGAAiPYfw6dyisNKYnjtMvP9WjPkuIezhQx4dI7HKJB8uKvT6xpV/0pEELeRM
# IUMQ40npJvt+75cKJd4Qcrk=
# SIG # End Windows Authenticode signature block