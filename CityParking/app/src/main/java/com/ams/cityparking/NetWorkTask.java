package com.ams.cityparking;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

class NetWorkTask extends AsyncTask<String,Void,Boolean>{
    private Intent intent;
    private AppCompatActivity activity;
    private String response;

    protected NetWorkTask(AppCompatActivity a, Intent i){
        this.intent = i;
        this.activity = a;
    }

    @Override
    protected Boolean doInBackground(String... strings) {
        Log.d("NetWorkTask","doing in background! " + strings[0]);
        // connect to server
        URL url;
        try {
            url = new URL("http://192.168.1.76:8000");
        }catch (MalformedURLException e) {
            Log.e("malformed url",e.toString());
            return false;
        }
        HttpURLConnection connection;
        try {
            connection = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            Log.e("url connection failed",e.toString());
            return false;
        }
        boolean result = true;
        try {
            InputStream in = new BufferedInputStream(connection.getInputStream());
            // read
            byte[] contents = new byte[1024];

            int bytesRead = 0;
            String strFileContents;
            while((bytesRead = in.read(contents)) != -1) {
                response += new String(contents, 0, bytesRead);
            }
        } catch (IOException e) {
            Log.e("reading buffer",e.toString());
            result = false;
        } finally {
            connection.disconnect();
        }
        return result;
    }

    @Override
    protected void onPostExecute(Boolean result) {
        if(result) {
            Log.d("NetWorkTask", "finished " + response);
        }else{
            Log.d("NetWorkTask", "woopsie!");
        }
        activity.startActivity(intent);
    }

}
