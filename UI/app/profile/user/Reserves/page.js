"use client"
import { useState, useEffect } from "react";
import { mockReservations } from "@/data/mockData";
import ReserveCardPaied from "@/components/layout/ReserveCardPaied";
import ReserveCardUnPaied from "@/components/layout/ReserveCardUnpaied";

export default function Reserves (){

       useEffect(()=>{
    // const getDetails = async ()=>{

    //     // const token = 
    //     const response = await fetch("", {
    //     headers: {
    //     Authorization: `Bearer ${token}`
    // }
    // });
    
    //     const result = await response.json()

    //     return result.data.active

    // }

    setData(mockReservations)

    },[])
    const [data, setData]=useState()


    return (
        data && <div className="flex flex-wrap gap-3 mt-25 flex-col justify-between p-5 w-7/12">
            {
                data.map((ticket)=>{
                    if(ticket.status=="paid"){
                        return <ReserveCardPaied key={ticket.reservation_id}  total_amount={ticket.total_amount} seats={ticket.seats} away_team_name={ticket.away_team_name} 
                        home_team_name={ticket.home_team_name} venue_name={ticket.venue_name} city_name={ticket.city_name}  event_datetime={ticket.event_datetime} paid_at={ticket.paid_at} reservation_id={ticket.reservation_id} />
                    } else if (ticket.status=="pending"){
                        return <ReserveCardUnPaied key={ticket.reservation_id} total_amount={ticket.total_amount} seats={ticket.seats} away_team_name={ticket.away_team_name} 
                        home_team_name={ticket.home_team_name} venue_name={ticket.venue_name} city_name={ticket.city_name}  event_datetime={ticket.event_datetime} remaining_seconds={ticket.remaining_seconds} reserved_at={ticket.reserved_at} reservation_id={ticket.reservation_id} />
                    } 
                })
            }
        </div>
    )
}