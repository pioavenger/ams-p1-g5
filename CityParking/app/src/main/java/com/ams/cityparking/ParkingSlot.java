package com.ams.cityparking;

public class ParkingSlot {
    //private String name;
    private String rating;
    private String cpmin;
    private String distance;
    private String sid;

    public ParkingSlot(String rating, String cpmin, String distance, String sid){
        //this.name = name;
        this.rating = rating;
        this.cpmin = cpmin;
        this.distance = distance;
        this.sid = sid;
    }

    //public String getName(){ return name; }

    public String getRating(){
        return rating;
    }

    public String getcpmin(){
        return cpmin;
    }

    public String getDistance(){
        return distance;
    }

    public String getsid(){
        return sid;
    }
}
