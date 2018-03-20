"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import math
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#




def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    
    maxspeed = [(1000, 26), (600, 28), (400, 30), (200, 32), (0, 34)]
    
    hr = 0
    mi = 0
    
    dist = control_dist_km
    
    if(control_dist_km <= 1.2*(brevet_dist_km)):
        
        if(control_dist_km > brevet_dist_km):
            dist = brevet_dist_km
    
        for category in maxspeed:
            division, speed = category
            if dist > division:
                distdiff = dist - division
                time = float(distdiff) / float(speed)
                hr+= distdiff // speed
                mi+= (time - (distdiff // speed))*60
                dist = division
        
        round(mi)
        rtrn = arrow.get(brevet_start_time)
        """
        print(rtrn.isoformat())
        print(hr)
        print(mi)
        """
        rtrn = (rtrn.shift(hours=+ hr, minutes=+mi)).isoformat()
        #print(rtrn)
        return rtrn
    else:
        return "err"

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    
    minspeed = [(1000, 13.333), (600, 11.428), (0, 15)]
    
    hr = 0
    mi = 0
    dist = control_dist_km
    
    if (control_dist_km <= 1.2*(brevet_dist_km)):
        
        if(control_dist_km > brevet_dist_km):
            dist = brevet_dist_km
            
    
        for category in minspeed:
            division, speed = category
            if dist > division:
                distdiff = dist - division
                time = float(distdiff) / float(speed)
                hr+= distdiff // speed
                mi+= (time - (distdiff // speed))*60
                dist = division
        
        rtrn = arrow.get(brevet_start_time)
        round(mi)
        
        if( ( (control_dist_km >= 200) and (control_dist_km <= 240) ) and (brevet_dist_km == 200)):
            hr = 13
            mi = 30
        
        return (rtrn.shift(hours=+ hr, minutes=+mi)).isoformat()
    else:
        return "err"
