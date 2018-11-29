package com.ams.cityparking;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

class LoginNetWorkTask extends NetWorkTask {
    private AppCompatActivity activity;
    private Intent intent;

    protected LoginNetWorkTask(String url,AppCompatActivity a, Intent i) {
        super(url);
        this.activity = a;
        this.intent = i;
    }

    @Override
    protected void onPostExecute(Boolean result) {
        // {"error": "OK", "email": email, "password": password}

        // convert payload to String
        String response = new String(payload, 0, payloadSize);

        // covert to json
        JSONObject json_response = null;
        try {
            json_response = new JSONObject(response);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // read json
        String error;
        try {
            // get error
            error = json_response.getString("error");
            if(error.equals("OK")){
                String email = json_response.getString("error");
                if(result) {
                    Log.d("NetWorkTask", "finished: " + email);
                }else{
                    Log.d("NetWorkTask", "woopsie!");
                }
                activity.startActivity(intent);
            }else if(error.equals("USER_NOT_FOUND_ERROR")){
                Toast toast = Toast.makeText(activity, "email not found!" ,Toast.LENGTH_SHORT);
                toast.show();
            }else if(error.equals("INCORRECT_PASSWORD_ERROR")){
                Toast toast = Toast.makeText(activity, "wrong password!" ,Toast.LENGTH_SHORT);
                toast.show();
            }else{ // MEMBER_ALREADY_ONLINE_ERROR
                Toast toast = Toast.makeText(activity, "already online!" ,Toast.LENGTH_SHORT);
                toast.show();
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
