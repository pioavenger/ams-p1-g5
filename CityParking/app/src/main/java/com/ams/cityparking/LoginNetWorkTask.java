package com.ams.cityparking;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONArray;
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
        if(!result){
            // cant connect
            Toast toast = Toast.makeText(activity, "no connection!" ,Toast.LENGTH_SHORT);
            toast.show();
            return;
        }
        // {"error": "OK", "email": email, "password": password}

        // convert payload to String
        Log.d("NetWorkTask",Integer.toString(payloadSize));
        String response = new String(payload, 0, payloadSize);
        try {
            // covert to json
            JSONArray array = new JSONArray(response);
            JSONObject json_response = (JSONObject) array.get(0);

           // read json
            String error;
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
