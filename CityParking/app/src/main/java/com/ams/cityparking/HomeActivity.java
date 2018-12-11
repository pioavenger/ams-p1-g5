package com.ams.cityparking;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.RadioButton;
import android.widget.TextView;

import com.ams.cityparking.NetWorkTools.LogoutNetWorkTask;
import com.ams.cityparking.fragments.BookFragment;
import com.ams.cityparking.fragments.BrowseFragment;
import com.ams.cityparking.fragments.HomeFragment;

public class HomeActivity extends AppCompatActivity {
    Fragment selectedFragment = null;

    private BottomNavigationView.OnNavigationItemSelectedListener navListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.nav_home:
                    selectedFragment = new HomeFragment();
                    break;
                case R.id.nav_browse:
                    selectedFragment = new BrowseFragment();
                    break;
                case R.id.nav_book:
                    selectedFragment = new BookFragment();
                    break;
            }
            getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container,selectedFragment).commit();
            return true;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.bottom_navigation);
        navigation.setOnNavigationItemSelectedListener(navListener);

        HomeFragment h = new HomeFragment();
        // initial fragment
        getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container,h).commit();
    }

    public void logout(View view) {
        // get email
        SharedPreferences sp = getSharedPreferences("login_prefs", MODE_PRIVATE);
        String email = sp.getString("email", "");

        LogoutNetWorkTask task = new LogoutNetWorkTask("/signout",this);
        String[] params = {"email=" + email};
        Log.d("CityParking-HA",email);
        // send
        task.execute(params);
    }

    public void onRadioButtonClicked(View view){
        SharedPreferences sp = getSharedPreferences("browse_prefs", MODE_PRIVATE);
        SharedPreferences.Editor editor = sp.edit();

        if (!((RadioButton) view).isChecked()){
            return;
        }
        // Check which radio button was clicked.
        switch (view.getId()) {
            case R.id.radio_button_price:
                Log.d("onRadioButtonClicked", "price");
                editor.putString("filter_type", "0");
                editor.commit();
                break;
            case R.id.radio_button_distance:
                Log.d("onRadioButtonClicked", "distance");
                editor.putString("filter_type", "1");
                editor.commit();
                break;
            case R.id.radio_button_rating:
                Log.d("onRadioButtonClicked", "rating");
                editor.putString("filter_type", "2");
                editor.commit();
                break;
            default:
                break;
        }
        ((BrowseFragment) selectedFragment).updateList();
    }
}
