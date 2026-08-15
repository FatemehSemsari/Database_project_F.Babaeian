"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import MatchCard from "@/components/layout/MatchCard";
import SearchFillter from "@/components/layout/SearchFillter";
import { mockMatches } from "@/data/mockData";


const groupEvent = Object.values(

    //fetch
    mockMatches.reduce((groups, data) =>{
        const eventId = data.event_id

        if(!groups[eventId]){
            groups[eventId] = []
        }
        groups[eventId].push(data)

        return groups
    }, {})

);

    

  const searchHandler = (sport , city, venue, dateto, datefrom, timeto, timefrom, name)=>{
        setFilltered(true)

        const filters = {
            sport_id :sport,
            team_id : name,
            city_id: city,
            venue_id : venue,
            date_from: datefrom,
            date_to : dateto
        }

        //fetch
    }



export default function Matches(){

    const [filltered , setFilltered] = useState(false)
    const [data , setData] = useState()
    const router = useRouter() 


    useEffect(() => {
        // getTeams().then(data =>{
        //   setTeams(data)
        //   console.log(data)
        //   setLoaded(true);
        // });

        setData(groupEvent)
      }, []);


     const clickHandler = (evenTicket)=>{
        sessionStorage.setItem(
            "selectedEvent",
            JSON.stringify(evenTicket)
        )
        router.push(`/match/${evenTicket[0].event_id}`)
    }

    return(
        <div className=" min-h-screen m-auto w-11/12">
            <SearchFillter></SearchFillter>
            <div className="mt-5 w-full flex flex-wrap justify-center items-center">
                {groupEvent.map((eventTicket) => {
                return <MatchCard clickHandler={clickHandler} eventTicket={eventTicket}  key={eventTicket[0].event_id} sport_name={eventTicket[0].sport_name} 
                venue_name={eventTicket[0].venue_name} away_team_name={eventTicket[0].away_team_name} away_team_logo={eventTicket[0].away_team_logo} home_team_name={eventTicket[0].home_team_name} home_team_logo={eventTicket[0].home_team_logo} event_date_time={eventTicket[0].event_datetime} 
                price={Math.min(...eventTicket.map(ticket => ticket.current_price))}></MatchCard>
            })}
            </div>
        </div>
    );
}