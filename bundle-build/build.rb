#!/bin/ruby

require 'yaml'
require 'fileutils'
require 'tmpdir'
require_relative "config"
require_relative "component_builder"

if ARGV.length != 1
	puts "Usage: ruby build.rb <path-to-config>"
	exit
end

file = ARGV[0]

config = Config.new(YAML.load_file(file))
ARCHITECTURE=Config.getArchitecture()
puts "Executing #{config.type} build for #{ARCHITECTURE}"

FileUtils.mkdir_p('build')

default_buildscripts=File.expand_path('./components')
outputDir=File.expand_path('./build')
workspace=Dir.pwd
Dir.mktmpdir do |dir|
  Dir.chdir(dir)
  # Checkout all components
  config.components.each{|component|
   component.checkout()
  }

  # Build all components in order
  builder=ComponentBuilder.new(default_buildscripts, outputDir)
  config.components.each{|component|
    builder.build_component(component, config.version, ARCHITECTURE)
  }

end
Dir.chdir(workspace)

# TODO: Pass components off for bundle assembly
