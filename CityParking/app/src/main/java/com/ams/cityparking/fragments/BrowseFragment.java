package com.ams.cityparking.fragments;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.ams.cityparking.BrowseAdapter;
import com.ams.cityparking.NetWorkTools.BrowseNetWorkTask;
import com.ams.cityparking.ParkingSlot;
import com.ams.cityparking.R;

import java.util.ArrayList;

public class BrowseFragment extends Fragment {
    private RecyclerView mrecycler_view;
    private RecyclerView.Adapter madapter;
    private RecyclerView.LayoutManager mLayout_manager;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_browse,container,false);
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        Log.d("BF","Setup recycler");
        mrecycler_view = getActivity().findViewById(R.id.content_wrapper);
        mrecycler_view.setHasFixedSize(true);
        mLayout_manager = new LinearLayoutManager(getActivity());
        mrecycler_view.setLayoutManager(mLayout_manager);

        // set default filter
        SharedPreferences sp = getActivity().getSharedPreferences("browse_prefs", getActivity().MODE_PRIVATE);
        SharedPreferences.Editor editor = sp.edit();
        editor.putString("filter_type", "1"); // distance
        editor.commit();
        
        updateList();
    }

    public void updateList(){
        Log.d("BF","onActivityCreated");
        // browse
        BrowseNetWorkTask task = new BrowseNetWorkTask("/browse",this,getLayoutInflater());
        // get email
        SharedPreferences sp = getActivity().getSharedPreferences("login_prefs", getActivity().MODE_PRIVATE);
        String email = sp.getString("email", "");
        // get filter
        sp = getActivity().getSharedPreferences("browse_prefs", getActivity().MODE_PRIVATE);
        String filter_type = sp.getString("filter_type", "");
        String[] params = {"email=" + email,"filter_type="+filter_type, "recent=0"};
        // send
        task.execute(params);
    }

    public void makeAdapter(ArrayList<ParkingSlot> array){
        Log.d("BF","makeAdapter");
        madapter = new BrowseAdapter(array);
        mrecycler_view.setAdapter(madapter);
    }
}
