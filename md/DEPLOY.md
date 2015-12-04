## Steps to Deploy

1. Make sure all of your "ready to merge" changes have been merged to develop
2. Make sure the version in the following files has been bumped on develop (try to follow the pattern that already exists in those files):
    * `bower.json`
    * `package.json`
3. Make sure a release branch has been branched off of develop for this version, reviewed, and merged into master.
4. Make sure a tag has been made from the state of master with the new version as its name.
5. Make sure you are deploying from master!
6. Hit the button with extreme caution.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/rcoughlin/NFL/tree/master)