This project follows semantic versioning.

Recommendation is to reference with knicknic/myq-garage-server:latest or knicknic/myq-garage-server:v1.

|  tag |Note   |
|---|---|
| :latest |  most recent stable |
|  :v1 | most recent v1  |
|  :v1.0.X |  a specific patch |

I suggest using :tag@sha256. When you add the sha256 to the end of the tag to give context for what it is. And you can use something like [dependabot](https://docs.github.com/en/free-pro-team@latest/github/administering-a-repository/configuration-options-for-dependency-updates#package-ecosystem) to ensure your sha256 is up-to-date with your tag.