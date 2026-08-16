import UserProfileMenu from "@/components/layout/UserProfileMenu";

export default function UserProfileLayout({ children }) {

  
  return (
     <div className="bg-[#F8FAFC]  flex flex-row-reverse justify-around">
        <UserProfileMenu />
        {children}
     </div>
    
  );
}