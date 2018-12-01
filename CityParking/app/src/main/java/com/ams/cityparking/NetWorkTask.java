package com.ams.cityparking;

import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.URL;

import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.io.IOException;

class NetWorkTask extends AsyncTask<String,Void,Boolean>{
    protected byte[] payload;
    protected int payloadSize = 0;
    private String urlstr;

    protected NetWorkTask(String url){
        this.urlstr = "http://"+url;
    }

    @Override
    protected Boolean doInBackground(String... paramaters) {
        // add parameters
        String new_urlstr = urlstr;
        if(paramaters.length != 0)
            new_urlstr += "?";

        for(String param : paramaters)
            new_urlstr+="&"+param;

        URL url;
        try {
            url = new URL(new_urlstr);
        }catch (MalformedURLException e) {
            return false;
        }

        // connect
        HttpURLConnection connection;
        try {
            connection = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            Log.d("CityParking","FAILED TO CONNECT");
            return false;
        }

        // read payload
        boolean result = true;
        try {
            InputStream in = new BufferedInputStream(connection.getInputStream());
            // read
            payload = new byte[1024];
            int bytesRead = 0;
            while((bytesRead = in.read(payload)) != -1)
                payloadSize += bytesRead;
        } catch (IOException e) {
            Log.d("CityParking","FAILED TO READ");
            result = false;
        } finally {
            connection.disconnect();
        }
        return result;
    }

}
