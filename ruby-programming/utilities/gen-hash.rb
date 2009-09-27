#!/usr/bin/env ruby

# Class of all Hashes, regardless of type. Performs validations, sends to 
# appropriate method.
#
class Hash
  def initialize(type, string)
    # Verify string is valid:
    if string.class != String:
      puts "#{string} needs to be a String."
      exit
    end
    @string = string

    # Verify type is valid and allowed:
    if type.class != String:
      puts "#{type} needs to be a String."
      exit
    end
    @type = type.downcase
    allowed = ["ssha", "sha1", "md5"]
    if not allowed.member? @type
      puts "#{@type} hash type not implemented."
      exit
    end
  end

  def create_hash
    @hash = eval("make_#{@type}(@string)")
  end

  attr_reader :hash, :string, :type

  def make_ssha(string)
    require 'sha1'
    require 'base64'
    hash = Base64.encode64(Digest::SHA1.digest("#{string}"+'salt')+'salt').chomp!
    return hash
  end

  def make_bcrypt(string)
    require 'bcrypt'
    hash = BCrypt::Password.create(string, :cost => 10)
    return hash
  end

  def make_sha1(string)
    require "sha1"
    hash = Digest::SHA1.hexdigest(string)
    return hash
  end

  def make_md5(string)
    require "md5"
    hash = MD5.hexdigest(string)
    return hash
  end

end


# Main flow control:
#
def main
  type = "sha1"
  string = "supersecret"
  hash = Hash.new(type, string)
  hash.create_hash

  puts "Plain: #{string}"
  puts "#{type} hash: #{hash.hash}"
  exit
end

if __FILE__ == $0
  main
end
