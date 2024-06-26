Changelog
=========

Version 1.0.0
-------------
- support sonata configs
- use ``$node_set`` instead of ``$target`` in target files
- combine different ``get_peak_amplitudes`` functions
- print warning if no pairs found
- change CV-validation to be simulation-config driven
- restrict ``bluecellulab>=2.6.2`` due to bugs in previous versions
- edge population needs to be given as a commandline parameter

  - ``projection`` is no longer used in pathway configs. To have the same behavior, pass the name of the edge population in commandline

- allow ``hold_V: null`` in pathway configs

  - if not given and clamping mode is ``current``, skip calculation of holding current and set ``hold_I = 0``

Version 0.5.1
-------------
- [NSETM-2064] removed usage of blueconfig
- [NSETM-2180] Require bglibpy >= 4.11.1

Version 0.5.0
-------------

- Pass multiple traces to efel at the same time (see NSETM-1780)
- Add CV-validation (supports both voltage and current clamp modes)
- Fix compatibility with BGLibPy>=4.7.2.

Version 0.4.1
-------------

- Better errors description for synaptic reversal potentials usage.
- Replace nose tests with pytest.
- Update documentation.

Version 0.4.0
-------------

- Update bluepy dependency to 2.1.0.
- Update bglibpy dependency to 4.4.27.
- Fix growing memory issues [NSETM-1356].
- Update documentation format.

Version 0.3.3
-------------

- Add a configuration parameter `min_trace_amplitude` to
  filter out synaptic failures before calculating mean PSPs [NSETM-1166].

Version 0.3.1
-------------

- Update bglibpy dependency to 4.3.15.

Version 0.3.0
-------------

- Changed `projection` argument of `simulation.run_pair_simulation` to `add_projections`. Now it
  is not possible to specify the exact projection to simulate. All projections get simulated.
  You still can specify which projection to query in `pathways.Pathway`. Nothing changed there.

Version 0.2.2
-------------

- Changed the simulation run. Now it always with forward_skip=False. Even if the config file
  was specifying ForwardSkip == True. In this case, omit a warning to warn the user.
- Removed python2 support
- Fix errors of config loading, docs building.
