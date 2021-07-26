from setuptools import setup

package_name = 'rqt_rt_preempt'

setup(
    name=package_name,
    version='0.0.0',
    # package_dir={'': 'rqt_rt_preempt'},
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/resource', ['resource/RosRtpreempt.ui']),
        ('share/' + package_name, ['plugin.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros2',
    maintainer_email='inflo@web.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rqt_rt_preempt = rqt_rt_preempt.main:main',
        ],
    },
)
