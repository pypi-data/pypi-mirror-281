import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudflared-tunnel",
    version="0.1.0",
    author="Ralf Rademacher and Luca Soldaini",
    description="Start a TryCloudflare Tunnel with a context manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UWUplus/soldni/python-cloudflare-tunnel",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='cloudflare tunnel python',
    install_requires=['requests'],
    py_modules=['cloudflared_tunnel'],
)
