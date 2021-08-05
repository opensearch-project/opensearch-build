require 'open3'
require 'fileutils'

##
# This class is used to build components required for a bundle.
# It will look for a build.sh script within a component's repository and if not present fall back to a default location specified.

class ComponentBuilder
  attr_reader :default_script_path, :output_path

  ##
  # Creates a new ComponentBuilder with the specified paths
  # @param default_script_path - Path to a directory that contains a build.sh for a particular component.
  # @param output_path - Path to a directory where all output artifacts will be placed.
  def initialize(default_script_path, output_path)
    @default_script_path=default_script_path
    @output_path=output_path
  end

  def get_build_script(component)
    script_path=File.expand_path("./#{component.name}/build/build.sh")
    if File.exists?(script_path)
      return script_path
    else
      default_path="#{default_script_path}/#{component.name}/build.sh"
      if File.exists?(default_path)
        return default_path
      else
        # default to standard gradle script
        return "#{default_script_path}/standard-gradle-build/build.sh"
      end
    end
  end

  def build_component(component, opensearch_version, platform)
    script_path=get_build_script(component)
    puts "building #{component.name} with #{script_path}"
    Dir.chdir(component.name) do
         command="#{script_path} #{opensearch_version} #{platform}"
         # Execute build and immediately flush any output to stdout
         Open3.popen2e(command) do |stdin, stdout, wait|
           Thread.new do
              stdout.each {|line| puts line }
           end
           exit_status = wait.value
           puts "EXIT STATUS #{exit_status}"
         end
         # copy component build output to ./build
         outputDir="#{component.name}-artifacts"
         puts File.expand_path("./#{outputDir}")
         if Dir.exists?(File.expand_path("./#{outputDir}"))
           FileUtils.cp_r("#{outputDir}/.", "#{output_path}", preserve: true)
         end
         puts "finished building #{component.name}"
    end
  end
end
