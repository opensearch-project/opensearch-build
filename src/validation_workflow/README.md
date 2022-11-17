#### Automate the Validation during Releases. 
The input requires a mandatory version number , optional --distribution types(tar,rpm,yum) and --platform type (currently uses only linux) to automatically download and verify the artifacts.

*Usage*
```
./validation.sh --version 2.3.0 --distribution rpm --platform linux 
```
The following options are available.

| name                   | description                                                         |
|------------------------|---------------------------------------------------------------------|
| version                | Accepts a mandatory version number.                                 |
| -d, --distribution     | Assigns the distribution type specifed by the user                  |
| -p, --platform         | Determines the platform type of the atrifacts.  		       |
| --verbose              | Show more verbose output.                                           |

