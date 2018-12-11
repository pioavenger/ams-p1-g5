package com.ams.cityparking.fragments;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.ams.cityparking.R;

public class HomeFragment extends Fragment {

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_home,container,false);
        // read login preferences
        Activity parent = getActivity();
        SharedPreferences sp = parent.getSharedPreferences("login_prefs", parent.MODE_PRIVATE);
        String username = sp.getString("username", "");
        // write welcome message
        ((TextView) v.findViewById(R.id.username_welcome_text)).append(username);
        return v;
    }
}
