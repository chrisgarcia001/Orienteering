# Usage: > ruby ilog_output_summarizer.rb <directory>
# Goes through a directory of ILOG outputs and builds a summarization CSV file.


def get_objective line
  if line =~ /OBJECTIVE:/
    parsed = line.split(' ')
    parsed.delete("\n")
    return parsed.last
  elsif line =~ /no solution/  
    return '' 
  end
  nil
end

def get_time line
  if line =~ /Total/
    parsed = line.split(' ')
    parsed.delete("\n")
    parsed.delete(" ")
    parsed.delete("sec.")
    return parsed.last
  end
  nil
end

def get_bound line
  if line and line.is_a?(String) and line =~ /%/	
	parsed = line.split(' ')
	parsed.delete("\n")
	parsed.delete(" ")
	return parsed[5] if parsed.length == 8 
  end
  nil
end

dir = ARGV[0]
text = 'Problem,Objective Function,Solution Time,Best Bound'
Dir::foreach(dir) do |f|
  if f =~ /.txt$/
    problem = f.split('')[0, f.split('').length - 4].join('')
    obj = nil
	bound = nil
    time = nil
    File.open(File.join(dir, f), "r") do |file|
      while (line = file.gets) do
        obj = get_objective(line) if line and !obj
		if line
			bnd = nil
			bnd = get_bound(line)
			bound = bnd if bnd 
		end
        time = get_time(line) if line and !time
      end
    end
    text += ["\n" + problem, obj, time, bound].join(',')
  end
end
File.open(File.join(dir, "summary.csv"), 'w') {|f| f.write(text) }
