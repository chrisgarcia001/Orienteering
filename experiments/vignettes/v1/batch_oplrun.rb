# Usage: > ruby batch_oplrun <model> <input directory> <output directory>
# ASSUMES: input directory ONLY contains .dat files

model = ARGV[0]
input_dir = ARGV[1]
output_dir = ARGV[2]
File.new("write.txt", "w+")  
Dir::foreach(input_dir) do |f|
	if f =~ /.dat$/
		ofile = f.split('')[0, f.split('').length - 4].join('') + '.txt'
		cmd = 'oplrun ' + model + ' ' + File.join(input_dir, f)
		output = eval('`' + cmd + '`')
		File.open(File.join(output_dir, ofile), 'w+') {|fl| fl.write(output) }
		puts 'Processed: ' + f
	end
end