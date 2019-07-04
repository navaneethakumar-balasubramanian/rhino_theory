from setuptools import setup, find_packages

setup(
    name="rhino_th",
    version="0.0.1",  # Upgrades, Updates, Fixes
    author="DataCloud",
    author_email="bruno@datacloud.com",
    packages=["theory"],
    include_package_data=True,
    install_requires=["numpy", "scipy", "dash", "plotly", "flask"],
    # entry_points="""
    # [console_scripts]
    #     rlp=rhino_lp.cli.cli:cli
    # """,
)
