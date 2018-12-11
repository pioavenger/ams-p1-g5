package com.ams.cityparking.NetWorkTools;

import android.app.Activity;
import android.util.Log;
import android.view.LayoutInflater;
import android.widget.Toast;

import com.ams.cityparking.ParkingSlot;
import com.ams.cityparking.fragments.BrowseFragment;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class BrowseNetWorkTask extends NetWorkTask {
    private BrowseFragment fragment;
    private Activity activity;

    public BrowseNetWorkTask(String url, BrowseFragment curr_f, LayoutInflater infl) {
        // rooturl + url
        super((curr_f.getActivity().getSharedPreferences("url_prefs", curr_f.getActivity().MODE_PRIVATE).getString("url", "")+url));
        this.fragment = curr_f;
        this.activity = curr_f.getActivity();
    }

    @Override
    public void onPostExecute(Boolean result) {
        // cant connect
        if(!result){
            Toast toast = Toast.makeText(activity, "no connection!" ,Toast.LENGTH_SHORT);
            toast.show();
            return;
        }

        // convert payload to String
        Log.d("Browse",Integer.toString(payloadSize));
        String response = new String(payload, 0, payloadSize);
        try {
            // {"error": "OK", "email": email, "sl": [...]}
            // covert to json
            JSONObject json_response = new JSONObject(response);

            String error;
            // get error
            error = json_response.getString("error");
            if(error.equals("OK")){
                String str_sl = json_response.getString("sl");
                JSONArray sl = new JSONArray(str_sl);

                ArrayList<ParkingSlot> parkingSlotList = new ArrayList<ParkingSlot>();
                for(int i = 0; i < sl.length(); i++){
                    JSONObject parkingProvider = sl.getJSONObject(i);
                    Log.d("Browse",parkingProvider.toString());
                    // add parking slot info
                    String name = parkingProvider.getString("provider");
                    String rating = parkingProvider.getString("rating");
                    String cpmin = parkingProvider.getString("cpmin");
                    String distance = parkingProvider.getString("distance");
                    String sid = parkingProvider.getString("sid");
                    ParkingSlot ps = new ParkingSlot(name,rating,cpmin,distance,sid);
                    parkingSlotList.add(ps);
                }
                fragment.makeAdapter(parkingSlotList);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
