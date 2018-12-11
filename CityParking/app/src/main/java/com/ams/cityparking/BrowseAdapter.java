package com.ams.cityparking;

import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.ArrayList;

public class BrowseAdapter extends RecyclerView.Adapter<BrowseAdapter.ParkingSlotViewHolder> {
    public static class  ParkingSlotViewHolder extends RecyclerView.ViewHolder{
        public TextView name;
        public TextView rating;
        public TextView cpmin;
        public TextView distance;

        public ParkingSlotViewHolder(@NonNull View itemView) {
            super(itemView);
            name = itemView.findViewById(R.id.name);
            rating = itemView.findViewById(R.id.rating);
            cpmin = itemView.findViewById(R.id.cpmin);
            distance = itemView.findViewById(R.id.distance);
        }
    }
    private ArrayList<ParkingSlot> parkingSlotList;

    public BrowseAdapter(ArrayList<ParkingSlot> array){
        this.parkingSlotList = array;
    }

    @NonNull
    @Override
    public ParkingSlotViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        View v = LayoutInflater.from(viewGroup.getContext()).inflate(R.layout.ps_item, viewGroup, false);
        ParkingSlotViewHolder vh = new ParkingSlotViewHolder(v);
        return vh;
    }

    @Override
    public void onBindViewHolder(@NonNull ParkingSlotViewHolder psViewHolder, int i) {
        ParkingSlot curr_item = parkingSlotList.get(i);
        psViewHolder.name.setText(curr_item.getName());
        psViewHolder.rating.setText(curr_item.getRating());
        psViewHolder.cpmin.append(curr_item.getcpmin()+"€");
        psViewHolder.distance.setText(curr_item.getDistance()+"m");
    }

    @Override
    public int getItemCount() {
        return parkingSlotList.size();
    }
}
