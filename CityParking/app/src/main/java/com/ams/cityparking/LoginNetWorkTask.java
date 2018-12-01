package com.ams.cityparking;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

class LoginNetWorkTask extends NetWorkTask {
    private AppCompatActivity activity;

    protected LoginNetWorkTask(String url,AppCompatActivity curr_a) {
        // rooturl + url
        super((curr_a.getSharedPreferences("url_prefs", curr_a.MODE_PRIVATE).getString("url", "")+url));
        this.activity = curr_a;
    }

    @Override
    protected void onPostExecute(Boolean result) {
        // cant connect
        if(!result){
            Toast toast = Toast.makeText(activity, "no connection!" ,Toast.LENGTH_SHORT);
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

            // read json
            // {"error": "OK", "email": email, "password": password}

            String error;
            // get error
            error = json_response.getString("error");
            if(error.equals("OK")){
                String email = json_response.getString("email");
                String username = json_response.getString("mname");

                // store locally
                SharedPreferences sp = activity.getSharedPreferences("login_prefs", activity.MODE_PRIVATE);
                SharedPreferences.Editor editor = sp.edit();
                editor.putString("email", email);
                editor.putString("username", username);
                editor.commit();

                // change to home activity
                Intent intent = new Intent(new Intent(activity, HomeActivity.class));
                activity.startActivity(intent);
                activity.finish();
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
