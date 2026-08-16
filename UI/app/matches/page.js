"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import MatchCard from "@/components/layout/MatchCard";
import SearchFillter from "@/components/layout/SearchFillter";
import { mockMatches } from "@/data/mockData";







export default function Matches(){



    const [filltered , setFilltered] = useState(false)
    const [data , setData] = useState()
    const router = useRouter() 

        

  const searchHandler = (sport , city, venue, dateto, datefrom, name)=>{
        setFilltered(true)

        const filters = {
            sport_id :sport,
            team_id : name,
            city_id: city,
            venue_id : venue,
            date_from: datefrom,
            date_to : dateto
        }
         const params = new URLSearchParams();

    if (sport && sport !== "-1") {
        params.append("sport_id", sport);
    }

    if (name && name !== "-1") {
        params.append("team_id", name);
    }

    if (city && city !== "-1") {
        params.append("city_id", city);
    }

    if (venue && venue !== "-1") {
        params.append("venue_id", venue);
    }

    if (datefrom) {
        params.append("date_from", datefrom);
    }

    if (dateto) {
        params.append("date_to", dateto);
    }


          const getTeams = async() =>{
           const res =  await fetch(`http://127.0.0.1:8000/api/tickets/search/?${params.toString()}`)
           const datas = await res.json()
           console.log(datas)


            const groupEvent = Object.values(
        datas.data.tickets.reduce((groups, data) =>{
        const eventId = data.event_id

            if(!groups[eventId]){
                groups[eventId] = []
            }
            groups[eventId].push(data)

            return groups
        }, {})

        );

      

        setData(groupEvent)
        
    }
      getTeams()
}



    useEffect(() => {

        const getTeams = async() =>{
           const res =  await fetch("http://127.0.0.1:8000/api/tickets/search/")
           const datas = await res.json()
           console.log(datas)
            const groupEvent = Object.values(
        datas.data.tickets.reduce((groups, data) =>{
        const eventId = data.event_id

            if(!groups[eventId]){
                groups[eventId] = []
            }
            groups[eventId].push(data)

            return groups
        }, {})

        );

        setData(groupEvent)
        }

        
        getTeams()
        console.log(data)
       
      }, []);


     const clickHandler = (evenTicket)=>{
        sessionStorage.setItem(
            "selectedEvent",
            JSON.stringify(evenTicket)
        )
        router.push(`/match/${evenTicket[0].event_id}`)
    }

    return(
        data && <div className="min-h-screen m-auto w-11/12">
            <SearchFillter searchHandler={searchHandler}></SearchFillter>
            <div className="mt-5 w-full flex flex-wrap justify-center items-center">
                {data.map((eventTicket) => {
                return <MatchCard clickHandler={clickHandler} eventTicket={eventTicket}  key={eventTicket[0].event_id} sport_name={eventTicket[0].sport_name} 
                venue_name={eventTicket[0].venue_name} away_team_name={eventTicket[0].away_team_name} away_team_logo={eventTicket[0].away_team_logo} home_team_name={eventTicket[0].home_team_name} home_team_logo={eventTicket[0].home_team_logo} event_date_time={eventTicket[0].event_datetime} 
                price={Math.min(...eventTicket.map(ticket => ticket.current_price))}></MatchCard>
            })}
            </div>
        </div>
    );
}