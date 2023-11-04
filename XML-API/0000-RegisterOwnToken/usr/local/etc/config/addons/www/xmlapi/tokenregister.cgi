#!/bin/tclsh
source session.tcl

puts "Content-Type: text/xml; charset=iso-8859-1"
puts ""
puts -nonewline "<?xml version='1.0' encoding='ISO-8859-1' ?><tokenregister>"

if {[info exists sid] && [check_session $sid]} {

  set token ""
  set desc ""
  set ise_id "-1"
  catch {
    set input $env(QUERY_STRING)
    set pairs [split $input &]
    foreach pair $pairs {
      if {0 != [regexp "^token=(.*)$" $pair dummy val]} {
        set token $val
        continue
      }
      if {0 != [regexp "^desc=(.*)$" $pair dummy val]} {
        set desc [regsub -all "%20" $val " "]
        continue
      }
    }
  }

  if {$token != ""} {
    set newToken [register_own_token $token $desc]
  } else {
    set newToken [register_token $desc]
  }

  if { $newToken != "" } {
    puts "<token desc='$desc'>$newToken</token>"
  } else {
    puts "<error/>"
  }

} else {
  puts -nonewline {<not_authenticated/>}
}
puts "</tokenregister>"
