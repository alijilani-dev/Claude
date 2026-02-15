docker build -f Dockerfile.dev -t task:dev .                            # python    dev     python-task
docker build -f Dockerfile.dev2 -t task:dev2 .                          # alpine    dev2    alpine-task
docker build -f Dockerfile.staging -t task:staging .                    # slim      staging staging-task
docker run -d -p 8000:8000 --name alpine-task task:dev2
docker run -d -p 8000:8000 --name

what if docker ps -> is fastapi actually running or getting some error?
what does this mean "Running pip as the 'root' user"
