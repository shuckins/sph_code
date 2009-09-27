require 'rubygems'
require 'feed_tools'

feed = FeedTools::Feed.open('http://dancingpenguinsoflight.com/feed')

puts "Title:", feed.title
puts "Link:", feed.link
puts "Description:", feed.description
puts "Feed time:", feed.time
puts "Updated: ", feed.updated

for item in feed.items
  puts item.methods
#   puts item.title
#   puts item.link
#   puts item.content
end
