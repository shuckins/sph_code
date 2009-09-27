#!/usr/bin/env ruby
require "rubygems"
require "builder"

builder = Builder::XmlMarkup.new
xml = builder.person { |b| b.name("Foo"); b.phone("111-111-1111") }
puts xml
