import exiftool
import os

from camera_handler import Camera

def get_image_meta(image_path):
    image_meta = {}
    with exiftool.ExifToolHelper() as et:
        try: 
            data = et.get_metadata(image_path)[0]
            image_meta["name"]  = os.path.basename(image_path)
            image_meta["path"]  = image_path
            image_meta["lat"]   = data["Composite:GPSLatitude"]
            image_meta["long"]  = data["Composite:GPSLongitude"]
            image_meta["alt"]   = data["Composite:GPSAltitude"]
            image_meta["yaw"]   = data["XMP:Yaw"]
            image_meta["pitch"] = data["XMP:Pitch"]
            image_meta["roll"]  = data["XMP:Roll"]
            image_meta["fov"]   = data["Composite:FOV"]
            image_meta["height"]= data["File:ImageHeight"]
            image_meta["width"] = data["File:ImageWidth"]
            image_meta["focal_length"] = data["EXIF:FocalLength"]
            image_meta["focal_plan_resolution"] = data["EXIF:FocalPlaneXResolution"]
            # HACK:FIXME: subtract the above-sea-level altitude with the ground elevation (average is 170m in Fahud and Yibal)
            image_meta["alt"] -= 170
            # TODO: by standard, only Above Sea Level (0) and Below Sea Level (not 0) is valid as the GPSAltitudeRef,
            # and it should be always Above Sea Level for this project (not underwater). To fix the hack,
            # we can deploy https://github.com/ajnisbet/opentopodata instance in our localhost, then hit the API to get
            # the ground elevation at a certain lat-lon.
            # There are a lot of public elevation datasets available mentioned in https://www.opentopodata.org/.
            # Also, we might be able to source our own LIDAR-surveyed dataset.
        except:
            image_meta = {}
    return image_meta


def get_visible_assets_in_image(image_meta, kmls):
    visible_kmls = []
    camera = Camera(
        width_fov_degrees=image_meta['fov'],
        image_width=image_meta['width'], 
        image_height=image_meta['height'], 
        focal_length_mm=image_meta['focal_length'],
        focal_plan_resolution=image_meta['focal_plan_resolution']
        )
    camera.set_position(image_meta['lat'], image_meta['long'], roll=image_meta['roll'], pitch=image_meta['pitch'], yaw=image_meta['yaw'], height_above_ground=image_meta["alt"])
    
    
    for id, coords in kmls.items():
        visible_points = []
        for gps_coords in coords:
            image_coords = camera.to_image_coords(asset_lat=gps_coords[1], asset_long=gps_coords[0], return_outside = False)
            if image_coords:
                visible_points.append({
                    "gps": gps_coords, 
                    "pixel": image_coords
                    })
    
        if len(visible_points) > 0:
            visible_kmls.append({"id": id, "kml": visible_points})
    
    return visible_kmls


