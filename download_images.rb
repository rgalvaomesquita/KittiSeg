#https://maps.googleapis.com/maps/api/streetview?size=400x400&location=40.720032,-73.988354&fov=90&heading=235&pitch=-90&key=
require 'google_maps_service'
require 'polylines'
require "open-uri"
require 'fileutils'
require 'addressable/uri'
require 'webrick/httputils'
require 'json'

$fileStreetsNames = 'streetnames.txt'
#$mapsapikey = ''
$mapsapikey = ''
$city = 'Olinda - PE'


def downloadStreetImages(subdir, streetname, pitch, flagVarpitch = false, flagVarHeading = false)

 boundPoints = getStreetBounds(streetname)
 if boundPoints.nil?
  puts "nil bound points"
  return nil
 end

 #for pointIter in 0..1
 for pointIter in [0]
     
     #polylines = getPolylinesFromOrigDest(boundPoints[pointIter],boundPoints[2])

     #points = Polylines::Decoder.decode_polyline(polylines)
     points = boundPoints
     flgDownload = false
     points.each{
      |point|
      
      urlRevGeocoding = "https://maps.googleapis.com/maps/api/geocode/json?latlng=#{point[0]},#{point[1]}&key=#{$mapsapikey}"
      urlRevGeocoding.force_encoding('binary')
      urlRevGeocoding=WEBrick::HTTPUtils.escape(urlRevGeocoding)


      a = JSON.load(open(urlRevGeocoding))
      

      results = a['results']
      if (results.nil? || results[0].nil? || results[0]['formatted_address'].nil?)
        
        puts "#{streetname}: error!"
        break
      end
      arrStName = streetname.split
      flgDownload = false
      arrStName.each{
        |subName|
        puts "formatted address: #{results[0]['formatted_address']} subName: #{subName}"

        if subName != 'de' and subName != 'da' and subName != 'do' and subName != 'Travessa' and subName != 'Avenida' and subName != 'Av.' and subName != 'Rua' and subName != 'R.'  and results[0]['formatted_address'].include? subName
          flgDownload = true
          break
        end
      }
      
      if flgDownload and results[0]['formatted_address'].include? $city
        puts "i am downloading this point!"

        if flagVarHeading
          for var_heading in [-1,0,45,90,135,180]
           downloadPointImage(subdir,point,var_heading,streetname, pitch)
          end
        else
           downloadPointImage(subdir,point,-1,streetname, pitch)
        end
      
      else
        puts "i am not downloading this point :( "
      end

      
     }

   end


end

def downloadPointImage(subdir, point, heading, streetname, pitch)

  if point.nil?
    return
  end
  urlp1='https://maps.googleapis.com/maps/api/streetview?size=400x400&location='
  urlp2='&fov=90'
  urlp3='&key='+$mapsapikey
  
  #url = "#{urlp1}#{point[0]},#{point[1]}#{urlp2}" 
  url = "#{urlp1}#{point[0]},#{point[1]}#{urlp2}" 
  url = url + "&pitch=#{pitch}"
  if heading >= 0
    url = url + "&heading=#{heading}"
  end
  #if pitch == 0
  #	url = url + '&pitch=-90'
  #else
  #	url = url + '&pitch=0'
  #end
  url+= urlp3;
  
  puts url 


  begin

      url.force_encoding('binary')
      url=WEBrick::HTTPUtils.escape(url)

      req = open(url)
      open("#{subdir}/#{point[0]}_#{point[1]}_heading=#{heading}.png", 'wb') do |file|
	  	file << req.read
	  end
	  
  rescue Exception => ex
       puts "An error of type #{ex.class} happened, message is #{ex.message}"
  end
 
end

def createDir(dirname)
	unless File.directory?(dirname)
  		puts 'creating directory '+dirname
  		FileUtils.mkdir_p(dirname)
	end
end

def getPolylinesFromOrigDest(orig, dest)
	gmaps = GoogleMapsService::Client.new(key: $mapsapikey)

	routes = gmaps.directions(
   "#{orig[0]},#{orig[1]}",
   "#{dest[0]},#{dest[1]}",
    mode: 'walking',
    alternatives: false)


	#puts routes
	return routes[0][:overview_polyline][:points]
end

def getStreetBounds(streetname)

	url = "https://maps.google.com/maps/api/geocode/json?address=#{streetname}, #{$city}&key=#{$mapsapikey}"
	url.force_encoding('binary')
	url=WEBrick::HTTPUtils.escape(url)


	a = JSON.load(open(url))
   
  if(!a["error_message"].nil? and a['error_message'].include? 'exceeded your daily request')
          puts "exiting the program: #{a['error_message']}"
          gets
          exit
  end
      
	results = a['results']

  if (results.nil? || results[0].nil? || results[0]['geometry'].nil?)
    return nil
  end
	bounds = results[0]['geometry']['bounds']
	points = []
  if bounds.nil?
    return nil
  end
  
	#bounds.each do |key,array|
	#	points.push([array['lat'],array['lng']])
	#end

  location = results[0]['geometry']['location']
 
  if location.nil?
    return points
  end
  
  points.push([location['lat'],location['lng']])
  #location.each do |key,array|
  #  puts key
  #  puts array
  #  points.push([array['lat'],array['lng']])
  #end
  

	return points
end


puts 'Downloading Street View Images...'



dirdataset = 'dataset_Olinda_pitch0_heading-1_noPolylines'



createDir (dirdataset)

File.open($fileStreetsNames,  "r:UTF-8").each do |line|
  #f.any? do |line|
    puts line
    arr = line.split
    streetname = ""
   
    arr.each do |word|
      if streetname == ""
        streetname = word
      else
        streetname = streetname  + " " + word
      end
    end
    dirStreet = dirdataset+'/'+streetname+ ''
    puts dirStreet
    #dirStreet = dirdataset+"/"+streetname
          
          createDir(dirStreet)
          downloadStreetImages(dirStreet, streetname, 0, false, false)
  #end
end



# File.open($fileStreetsNames,  "r:UTF-8") do |f|
#   f.any? do |line|
  	
#     arr = line.split
#     puts line
    
#     streetname = ""
#     arr.each do |word|
		
#         puts word
#         if ['residencial', 'não', 'classificados', 'passeio', 'pedestre', 'primário', 'secundário', 'terciário'].include? word
#         	if streetname.size > 0
#     			puts streetname

#           dirStreet = dirdataset+'/'+streetname
          
#           createDir(dirStreet)
#     			#downloadStreetImages(dirStreet, streetname, -90)

#           #dirView = dirnameview+'/'+streetname
#           #createDir(dirView)
#     			#downloadStreetImages(dirView, streetname, 1)

#     			streetname = ""
#     		  end
#         else
#           if streetname.size > 0
#         	 streetname = streetname + " "+ word; 
#           else
#             streetname = word;
#           end
#         end
#         #puts "digite qq coisa"
#         #gets
#     end
   
#   end
# end

puts 'Finished!'
