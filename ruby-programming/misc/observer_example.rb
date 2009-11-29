#!/usr/bin/env ruby
# From http://www.oreillynet.com/ruby/blog/2006/01/ruby_design_patterns_observer.html

require 'observer'  # Key step 1

class MyObservableClass
  include Observable  # Key step 2

  def do_thing
    changed  # note that our state has changed
    result = "The answer is 42!"
    notify_observers(result)
  end
end

class MyObserverClass
  def update(new_data)  # Key step 3
    puts "The new data: #{new_data}"
  end
end

watched = MyObservableClass.new
watched.add_observer(MyObserverClass.new)
watched.do_thing
