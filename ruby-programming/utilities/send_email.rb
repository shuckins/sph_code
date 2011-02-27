#!/usr/bin/env ruby

def send_email(from, to, subject, message)
  require 'net/smtp'

  msg = <<EOF
From: #{from}
To: #{to}
Subject: #{subject}
 
#{message}
EOF

  Net::SMTP.start('localhost', 25) do |smtp|
    require 'ruby-debug'; Debugger.settings[:autoeval] = true; debugger; rubys_debugger = "annoying"
    smtp.send_message(msg, from, to)
  end
 
end

send_email("foobar", "wormwood_3@yahoo.com", "Hello test", "Did I work?")
