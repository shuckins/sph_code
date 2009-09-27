#!/usr/bin/env ruby
require 'rubygems'
require 'log4r'
include Log4r
 
log_file = 'sample.log'
 
log = Logger.new 'sample application'
console_format = PatternFormatter.new(:pattern => "%l:\t %m")
log.add Log4r::StdoutOutputter.new('console', :formatter=>console_format)
 
file_format = PatternFormatter.new(:pattern => "[ %d ] %l\t %m")
log.add FileOutputter.new('fileOutputter', :filename => log_file, :trunc => false, :formatter=>file_format)
 
log.info 'sample application logging to console'
