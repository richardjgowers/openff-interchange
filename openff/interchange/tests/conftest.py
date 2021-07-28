def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # do not error based on number of skipped tests if running "minimal" tests
    if "not slow" not in terminalreporter.config.option.markexpr:
        if "skipped" in terminalreporter.stats:
            num_skipped_tests = len(terminalreporter.stats["skipped"])
            # TODO: Better way of detecting if this run is in "minimal" set
            from conda.cli.python_api import run_command

            if "gromacs" in run_command("list"):
                if num_skipped_tests > 120:
                    raise Exception(f"Too many skipped tests: {num_skipped_tests}")
