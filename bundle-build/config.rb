##
# This class is used to parse config used during a bundle build
class Config
    attr_reader :type, :version, :components
    def initialize(hash)
        @type = hash['type']
        @version = hash['version']
        @components = hash['components'].map{|component| Component.new(component)}
    end

    def self.getArchitecture()
      arch=`uname -m`.strip
      return case arch
      when 'x86_64'
          :'x64'
      when 'aarch64', 'arm64'
          :'arm64'
      else
          puts "Building on unsupported Architecture #{arch}, only x64 and arm64 are supported"
          exit
      end
    end
end

class Component
    attr_reader :name, :repository, :ref
    def initialize(hash)
        @name = hash['name']
        @repository = hash['repository']
        @ref = hash['ref']
    end

    def checkout()
        `git clone #{repository} #{name}`
        currentDir=Dir.pwd
        Dir.chdir(name)
        `git checkout #{ref}`
        Dir.chdir(currentDir)
    end
end
