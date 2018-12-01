package com.ams.cityparking;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class SignupNetWorkTask extends NetWorkTask {
    private AppCompatActivity activity;

    protected SignupNetWorkTask(String url, AppCompatActivity curr_a) {
        // rooturl + url
        super((curr_a.getSharedPreferences("url_prefs", curr_a.MODE_PRIVATE).getString("url", "")+url));
        this.activity = curr_a;
    }

    @Override
    protected void onPostExecute(Boolean result) {
        // cant connect
        Toast toast;
        if(!result){
            toast = Toast.makeText(activity, "no connection!" ,Toast.LENGTH_SHORT);
            toast.show();
            return;
        }

        // convert payload to String
        Log.d("NetWorkTask",Integer.toString(payloadSize));
        String response = new String(payload, 0, payloadSize);
        try {
            // covert to json
            JSONArray array = new JSONArray(response);
            JSONObject json_response = (JSONObject) array.get(0);

            String error;
            // get error
            error = json_response.getString("error");
            if(error.equals("OK")){
                // change to home activity
                Intent intent = new Intent(new Intent(activity, LoginActivity.class));
                toast = Toast.makeText(activity, "success!" ,Toast.LENGTH_SHORT);
                toast.show();
                activity.startActivity(intent);
                activity.finish();
            }else if(error.equals("WRONG_EMAIL_FORMAT_ERROR")){
                toast = Toast.makeText(activity, "wrong email format!" ,Toast.LENGTH_SHORT);
                toast.show();
            }else if(error.equals("WRONG_CARPLATE_FORMAT_ERROR")){
                toast = Toast.makeText(activity, "wrong carplate format!" ,Toast.LENGTH_SHORT);
                toast.show();
            }else if(error.equals("EMAIL_USED_ERROR")){
                toast = Toast.makeText(activity, "email already used!" ,Toast.LENGTH_SHORT);
                toast.show();
            }else{ //PASSWORD_MISMATCH_ERROR
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
