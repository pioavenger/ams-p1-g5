package com.ams.cityparking;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

class LogoutNetWorkTask extends NetWorkTask {
    private AppCompatActivity activity;

    protected LogoutNetWorkTask(String url,AppCompatActivity curr_a) {
        // roorurl + url
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

        SharedPreferences sp = activity.getSharedPreferences("login_prefs", activity.MODE_PRIVATE);
        SharedPreferences.Editor editor = sp.edit();
        editor.putString("email", "");
        editor.putString("username", "");
        editor.commit();

        // change to main activity
        Intent intent = new Intent(activity, MainActivity.class);
        activity.startActivity(intent);
        activity.finish();
    }
}
