from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    src_dir = os.getcwd()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            vertex_shader = os.path.join( self.src_dir, "sample.vert")
            fragment_shader = os.path.join( self.src_dir, "sample.frag")

            bin_path = os.path.join("bin", "test_package")
            self.run(bin_path + " -V " + vertex_shader, run_environment=True)

            bin_path = os.path.join("bin", "test_package.2")
            self.run(bin_path + " " + vertex_shader + " " + fragment_shader, run_environment=True)
