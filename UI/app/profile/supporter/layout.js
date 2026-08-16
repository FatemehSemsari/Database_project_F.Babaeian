import SupporterProfileMenu from "@/components/layout/SupporterProfileMenu";
export default function SupporterProfileLayout({ children }) {


  return (
       <div className="bg-[#F8FAFC] flex flex-row-reverse justify-around">
          <SupporterProfileMenu/>
          {children}
       </div>
      
    );
}