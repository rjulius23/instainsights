"""Main application window."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional, Protocol, Callable

from src.domain.models.profile import Profile


class ProfileServiceProtocol(Protocol):
    """Protocol for profile service."""
    
    def get_profile(self, username: str) -> tuple[Optional[Profile], Optional[str]]:
        """Get a profile by username."""
        ...
    
    def search_profiles(self, query: str) -> tuple[Optional[List[Profile]], Optional[str]]:
        """Search for profiles matching the query."""
        ...


class ExporterProtocol(Protocol):
    """Protocol for data exporters."""
    
    def export_profiles(self, profiles: List[Profile], filepath: str) -> None:
        """Export profiles to a file."""
        ...


class MainWindow(ttk.Frame):
    """Main application window."""
    
    def __init__(
        self,
        master: tk.Tk,
        profile_service: ProfileServiceProtocol,
        exporter: ExporterProtocol
    ) -> None:
        """
        Initialize the main window.
        
        Args:
            master: The root Tkinter window
            profile_service: Service for profile operations
            exporter: Service for exporting data
        """
        super().__init__(master)
        self.master = master
        self._profile_service = profile_service
        self._exporter = exporter
        self._profiles: List[Profile] = []
        
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create and arrange UI widgets."""
        # Search frame
        search_frame = ttk.LabelFrame(self, text="Search Profiles")
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        
        self._username_var = tk.StringVar()
        username_entry = ttk.Entry(search_frame, textvariable=self._username_var, width=30)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        username_entry.bind("<Return>", lambda e: self._search_profile())
        
        ttk.Button(
            search_frame,
            text="Search",
            command=self._search_profile
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(self, text="Profile Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create treeview for results
        columns = (
            "username", "full_name", "followers", "following", "avg_post_likes",
            "avg_post_comments", "avg_post_reshares", "recent_posts", "verified"
        )
        self._results_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            selectmode="extended"
        )
        
        # Define headings
        self._results_tree.heading("username", text="Username")
        self._results_tree.heading("followers", text="Followers")
        self._results_tree.heading("following", text="Following")
        self._results_tree.heading("avg_post_likes", text="Avg Post Likes")
        self._results_tree.heading("avg_post_comments", text="Avg Post Comments")
        self._results_tree.heading("avg_post_reshares", text="Avg Post Reshares")
        self._results_tree.heading("recent_posts", text="Recent Posts")
        self._results_tree.heading("verified", text="Verified")
        self._results_tree.heading("full_name", text="Full Name")

        
        # Define columns
        self._results_tree.column("username", width=80)
        self._results_tree.column("followers", width=60, anchor=tk.E)
        self._results_tree.column("following", width=60, anchor=tk.E)
        self._results_tree.column("avg_post_likes", width=120, anchor=tk.E)
        self._results_tree.column("avg_post_comments", width=120, anchor=tk.E)
        self._results_tree.column("avg_post_reshares", width=120, anchor=tk.E)
        self._results_tree.column("recent_posts", width=60, anchor=tk.E)
        self._results_tree.column("verified", width=60, anchor=tk.CENTER)
        self._results_tree.column("full_name", width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self._results_tree.yview)
        self._results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self._results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Details frame
        details_frame = ttk.LabelFrame(self, text="Profile Details")
        details_frame.pack(fill=tk.X, pady=5)
        
        self._details_text = tk.Text(details_frame, height=6, wrap=tk.WORD)
        self._details_text.pack(fill=tk.X, padx=5, pady=5)
        self._details_text.config(state=tk.DISABLED)
        
        # Bind selection event
        self._results_tree.bind("<<TreeviewSelect>>", self._on_profile_selected)
        
        # Actions frame
        actions_frame = ttk.Frame(self)
        actions_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            actions_frame,
            text="Export to CSV",
            command=self._export_to_csv
        ).pack(side=tk.RIGHT, padx=5)
    
    def _search_profile(self) -> None:
        """Search for a profile by username."""
        username = self._username_var.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        # Clear existing results
        for item in self._results_tree.get_children():
            self._results_tree.delete(item)
        
        self._profiles = []
        self._details_text.config(state=tk.NORMAL)
        self._details_text.delete(1.0, tk.END)
        self._details_text.config(state=tk.DISABLED)
        
        # Show loading indicator
        self.master.config(cursor="watch")
        self.update()
        
        try:
            # Try exact match first
            profile, error = self._profile_service.get_profile(username)
            
            if profile:
                self._profiles = [profile]
                self._display_profiles([profile])
            elif error:
                # If exact match fails, try search
                profiles, search_error = self._profile_service.search_profiles(username)
                
                if profiles:
                    self._profiles = profiles
                    self._display_profiles(profiles)
                else:
                    messagebox.showerror("Error", search_error or "No profiles found")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Reset cursor
            self.master.config(cursor="")
    
    def _display_profiles(self, profiles: List[Profile]) -> None:
        """Display profiles in the treeview."""
        for profile in profiles:
            stats = profile.statistics
            eng_stats = profile.engagement_stats
            
            self._results_tree.insert(
                "",
                tk.END,
                values=(
                    profile.username,
                    profile.full_name or "",
                    f"{stats.followers_count:,}",
                    f"{stats.following_count:,}",
                    f"{eng_stats.recent_avg_post_likes:.1f}",
                    f"{eng_stats.recent_avg_post_comments:.1f}",
                    f"{eng_stats.recent_avg_post_reshares:.1f}",
                    f"{eng_stats.recent_post_count}",
                    "✓" if profile.is_verified else "✗"
                )
            )
    
    def _on_profile_selected(self, event) -> None:
        """Handle profile selection event."""
        selection = self._results_tree.selection()
        if not selection:
            return
            
        # Get the selected item
        item = selection[0]
        username = self._results_tree.item(item, "values")[0]
        
        # Find the profile
        profile = next((p for p in self._profiles if p.username == username), None)
        if not profile:
            return
            
        # Update details text
        self._details_text.config(state=tk.NORMAL)
        self._details_text.delete(1.0, tk.END)
        
        stats = profile.statistics
        eng_stats = profile.engagement_stats
        details = (
            f"Username: @{profile.username}\n"
            f"Name: {profile.full_name or 'N/A'}\n"
            f"Bio: {profile.bio or 'N/A'}\n"
            f"Account: {'Private' if profile.is_private else 'Public'}"
            f"{', Verified' if profile.is_verified else ''}\n"
            f"Stats: {stats.followers_count:,} followers, {stats.following_count:,} following, "
            f"Engagements: {eng_stats.recent_avg_post_likes:.1f} avg likes, {eng_stats.recent_avg_post_comments:.1f} avg comments, "
            f"{eng_stats.recent_post_count:,} posts recently\n"
            f"Avg comments: {stats.avg_comments:.1f}"
        )
        
        self._details_text.insert(tk.END, details)
        self._details_text.config(state=tk.DISABLED)
    
    def _export_to_csv(self) -> None:
        """Export profiles to CSV file."""
        if not self._profiles:
            messagebox.showerror("Error", "No profiles to export")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
            
        try:
            self._exporter.export_profiles(self._profiles, filepath)
            messagebox.showinfo("Success", f"Exported {len(self._profiles)} profiles to {filepath}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
