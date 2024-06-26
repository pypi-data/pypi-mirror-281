ChangeLog
=========

0.2.8
- Update NeuroM dependency to version >= 3
- Use pytest for tests instead of nosetests

-----

0.2.7
-----

- Allow to pass numpy rangom generators ``yield_clones``.
- Fix the recursive pass of ``rng`` in ``scale_section``, ``_recursive_rotational_jitter``


0.2.6
-----

- Allow to pass numpy rangom generators to jitter functions

0.1.6
-----

- create_clones renamed to iter_clones. It now returns a generator of morphio.mut.Morphology clones.

0.1.5
-----

- Add Scaling CLI

0.1.4
-----

- Remove tqdb progress bar when running create_clones

0.1.3
-----

- Add seed argument to create_clones
- Allow default RotationParameters and use tqdm

0.1.1
-----

- create_clones returns the list of clone filenames

0.1.0
-----

- Add MorphClone functionality
- Add a web app to shrink an axon
- axon_shrinker: a tool to shrink an axon by splicing its middle part.
