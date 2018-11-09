from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from shutil import copyfile
import os

class OpencoreamrConan(ConanFile):
    name = "opencore-amr"
    version = "0.1.5"
    description = "OpenCORE Adaptive Multi Rate (AMR) speech codec library implementation."
    url = "https://github.com/conan-multimedia/opencore-amr."
    homepage = "https://sourceforge.net/projects/opencore-amr/"
    license = "Apachev2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"

    def source(self):
        #http://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-%(version)s.tar.gz'

        tools.get('http://172.16.64.65:8081/artifactory/gstreamer/{name}-{version}.tar.gz'.format(name=self.name, version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            _args = ["--prefix=%s/builddir"%(os.getcwd()), "--disable-silent-rules", "--enable-introspection"]
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=_args)
            autotools.make(args=["-j4"])
            autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))
                
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

