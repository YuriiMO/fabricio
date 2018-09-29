# Fabricio: Building Docker images

This example shows how to deploy configuration consisting of a single container based on custom image which automatically built from provided [Dockerfile](Dockerfile).

## Requirements
* Fabricio 0.4.6 or greater
* [Vagrant](https://www.vagrantup.com)
* One from the [list of Vagrant supported providers](https://www.vagrantup.com/docs/providers/) (this example was tested with [VirtualBox](https://www.virtualbox.org/))
* [Docker](https://www.docker.com/products/overview) for Linux/Mac/Windows
* Docker registry which runs locally on 5000 port, this can be reached out by executing following docker command: `docker run --name registry --publish 5000:5000 --detach registry:2`

## Files
* __Dockerfile__, used for building image
* __fabfile.py__, Fabricio configuration
* __README.md__, this file
* __Vagrantfile__, Vagrant config

## Virtual Machine creation

Run `vagrant up` and wait until VM will be created.

## List of available commands

    fab --list

## Deploy

    fab app
    
## Parallel execution

Any Fabricio command can be executed in parallel mode. This mode provides advantages when you have more then one host to deploy to. Use `--parallel` option if you want to run command on all hosts simultaneously:

    fab --parallel app

## Customization

See also "Hello World" [Customization](../hello_world/#customization) section.

### Custom `Dockerfile`

You can provide custom folder with `Dockerfile` by passing `build_path` parameter to `ImageBuildDockerTasks`:

```python
from fabricio import tasks

nginx = tasks.ImageBuildDockerTasks(
    # ...
    build_path='path/to/folder/with/dockerfile',
)
```
    
### Custom build params

Any `docker build` option can be passed directly to `prepare` command*:

    fab app.prepare:tag,file=my-Dockerfile,squash=yes
    
*\* Fabricio uses `--pull` and `--force-rm` options by default. However, these can be revoked: `prepare:pull=no,force-rm=no`.*

If you wish use custom `docker build` options then you have to call `push` and `upgrade` commands manually to finish deploy:

    fab app.push:tag
    fab app.upgrade:tag

Or, all in one line:

    fab app.prepare:tag,file=my-Dockerfile,squash=yes app.push:tag app.upgrade:tag

*See also how's Fabric work with [per-task arguments](http://docs.fabfile.org/en/1.14/usage/fab.html#per-task-arguments).*

## Issues

* Windows users may fall into trouble with `VirtualBox` and `Hyper-V`, the latter is used by "native" Docker for Windows. Try to disable Hyper-V and use [Docker Toolbox](https://www.docker.com/products/docker-toolbox) instead in such case
