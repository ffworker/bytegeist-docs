# Documentation System

This public repository owns only global, cross-repository documentation
workflow and orchestration explanation. Technical documentation remains in its
canonical source repository:

- applications → their own README/docs;
- infrastructure operations → `infra-configs`;
- learning and labs → `cka-lab`;
- global workflow explanation → this repository.

The source manifest declares participating repositories and paths. Trusted
workflows retrieve those paths into a transient workspace, build the private
site, and discard the generated files. No imported content is committed here.
