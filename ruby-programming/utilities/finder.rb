#!/usr/bin/env ruby
# Script used for a particular extraction task, but has some useful 
# examples of working with files and directories.

require 'find'
require 'ftools'

def extract_docs_with_images(dump_path)
  # Dir where docs with images will be copied
  flat_dump = "/home/shuckins/extracted_docs_with_images"
  if File.directory?(flat_dump)
    FileUtils.rm_rf(flat_dump)
    Dir.mkdir(flat_dump)
  else
    Dir.mkdir(flat_dump)
  end

  # Find all document dirs with image folders with content
  docs_with_images = []
  Find.find(dump_path) do |ent|
    if File.directory?(ent) and File.basename(ent) == "images" and not Dir.entries(ent) == ["..", "."]
      puts "Found #{ent} dir with images."
      # Add dir for doc in flat dir
      doc_dir = "#{flat_dump}/#{ent.split("/")[-2]}"
      Dir.mkdir(doc_dir)
      # Copy in images
      imgs = []
      Dir.foreach(ent) { |img| imgs << img unless img[0].chr == "."}
      imgs.each do |img|
        File.copy("#{ent}/#{img}", doc_dir, verbose=true)
      end
      puts "Copied images to #{flat_dump}."
    end
  end
end
