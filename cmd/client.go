package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
)

// clientCmd represents the client command
var clientCmd = &cobra.Command{
	Use:   "client",
	Short: "Manage clients and access",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		usage := cmd.UsageFunc()
		usage(cmd)
	},
}

// clientAddCmd
var clientAddCmd = &cobra.Command{
	Use:   "add",
	Short: "Add a user to a client by email address",
	Long:  `Add a user to an existing client by email address`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("client add called")
		verbose, _ := cmd.Flags().GetBool("verbose")
		fmt.Printf("Verbose: %t\n", verbose)
	},
}

// clientCreateCmd
var clientCreateCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a new client",
	Long:  `Create a new client`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("client create called")
	},
}

func init() {
	clientCmd.AddCommand(clientAddCmd, clientCreateCmd)
	RootCmd.AddCommand(clientCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// clientCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// clientCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
