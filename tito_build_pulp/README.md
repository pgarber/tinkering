Alternative version for --test builds with tito
=====
Tito allows us to build RPMs from git.  
Typically we would need to "tag" a commit, yet use of the --test flag will tell tito to build the latest git commit.  
Tito will typically change the version of the .spec to be based on the git hashtag.  
This causes some problems when building pulp-server and pulp_rpm which are in different git repos and hence their --test builds will have different hashes.  

Workaround
=====
 * This workaround will change the behavior of how tito forms the version of a --test build.  We will patch this behavior in the the "tito_mod" command
 1. Create a file at: ~/tito/build  
   ```echo 1 > ~/tito/build```
   2. ```cp tito_mod /usr/bin```
   3. Run 'test_build_pulp.sh`



Thanks to Jeff Ortel for sharing this workaround


