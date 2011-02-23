# This class represents the user's vocabulary. It provides methods to
# create a vocabulary, add to an existing one, print out statistics,
# and store a vocabulary on the filesystem.
class Vocabulary

  def initialize
    # Array to hold all words
    @vocabulary = []
  end

  def help
    help = "Enter as many words as you want, pressing Enter after each.
Enter ':listall' to print out the words entered thus far.
Enter ':exit' to exit the application.
Enter ':count' to get a count of words entered thus far.
Enter ':help' to print out this text."

    puts help
    puts
  end

  def stat_count
    puts "\nCount of words entered thus far: #{@vocabulary.length}\n\n"
  end

  def collect_words
    # Get initial input
    last = gets.chomp

    until last == ":exit"
      if last == ":listall"
        puts "\nWords entered so far:"
        p @vocabulary.sort
        puts
      elsif last == ":count"
        self.stat_count
      elsif last == ":help"
        self.help
      else
        @vocabulary << last
      end

      last = gets.chomp
    end
    self.exit
  end

  def exit
    puts "#------------------------------------------------------------------------------"
    puts "Here's what you entered:"
    p @vocabulary.sort
    puts "\nThanks for playing!"
  end

end
