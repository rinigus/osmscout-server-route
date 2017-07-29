#include <thread>
#include <functional>
#include <string>
#include <list>
#include <set>
#include <iostream>
#include <unordered_set>
#include <memory>
#include <stdexcept>
#include <sstream>

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

#include <prime_server/prime_server.hpp>
#include <prime_server/http_protocol.hpp>
using namespace prime_server;

#include "valhalla/midgard/logging.h"
#include "valhalla/midgard/util.h"

//#include "valhalla/loki/service.h"
//#include "valhalla/thor/service.h"
//#include "valhalla/odin/service.h"
//#include "valhalla/tyr/service.h"

namespace valhalla {
  namespace loki { extern void run_service(const boost::property_tree::ptree& config); }
  namespace thor { extern void run_service(const boost::property_tree::ptree& config); }
  namespace odin { extern void run_service(const boost::property_tree::ptree& config); }
  namespace tyr { extern void run_service(const boost::property_tree::ptree& config); }
}

int valhalla_route_service_main(int argc, char** argv) {

  if(argc < 2) {
    LOG_ERROR("Usage: " + std::string(argv[0]) + " config/file.json [concurrency]");
    return 1;
  }

  //config file
  //TODO: validate the config
  std::string config_file(argv[1]);
  boost::property_tree::ptree config;
  boost::property_tree::read_json(config_file, config);

  //grab the endpoints
  std::string listen = config.get<std::string>("httpd.service.listen");
  std::string loopback = config.get<std::string>("httpd.service.loopback");
  std::string interrupt = config.get<std::string>("httpd.service.interrupt");
  std::string loki_proxy = config.get<std::string>("loki.service.proxy");
  std::string thor_proxy = config.get<std::string>("thor.service.proxy");
  std::string odin_proxy = config.get<std::string>("odin.service.proxy");
  std::string tyr_proxy = config.get<std::string>("tyr.service.proxy");
  //TODO: add multipoint accumulator worker

  //check the server endpoint
  if(listen.find("tcp://") != 0) {
    if(listen.find("icp://") != 0) {
      LOG_ERROR("You must listen on either tcp://ip:port or ipc://some_socket_file");
      return EXIT_FAILURE;
    }
    else
      LOG_WARN("Listening on a domain socket limits the server to local requests");
  }

  //configure logging
  boost::optional<boost::property_tree::ptree&> logging_subtree = config
      .get_child_optional("tyr.logging");
  if (logging_subtree) {
    auto logging_config = valhalla::midgard::ToMap<
        const boost::property_tree::ptree&,
        std::unordered_map<std::string, std::string> >(logging_subtree.get());
    valhalla::midgard::logging::Configure(logging_config);
  }

  //number of workers to use at each stage
  auto worker_concurrency = std::thread::hardware_concurrency();
  if(argc > 2)
    worker_concurrency = std::stoul(argv[2]);

  //setup the cluster within this process
  zmq::context_t context;
  std::thread server_thread = std::thread(std::bind(&http_server_t::serve,
    http_server_t(context, listen, loki_proxy + "_in", loopback, interrupt, true)));

  //loki layer
  std::thread loki_proxy_thread(std::bind(&proxy_t::forward, proxy_t(context, loki_proxy + "_in", loki_proxy + "_out")));
  loki_proxy_thread.detach();
  std::list<std::thread> loki_worker_threads;
  for(size_t i = 0; i < worker_concurrency; ++i) {
    loki_worker_threads.emplace_back(valhalla::loki::run_service, config);
    loki_worker_threads.back().detach();
  }

  //thor layer
  std::thread thor_proxy_thread(std::bind(&proxy_t::forward, proxy_t(context, thor_proxy + "_in", thor_proxy + "_out")));
  thor_proxy_thread.detach();
  std::list<std::thread> thor_worker_threads;
  for(size_t i = 0; i < worker_concurrency; ++i) {
    thor_worker_threads.emplace_back(valhalla::thor::run_service, config);
    thor_worker_threads.back().detach();
  }

  //odin layer
  std::thread odin_proxy_thread(std::bind(&proxy_t::forward, proxy_t(context, odin_proxy + "_in", odin_proxy + "_out")));
  odin_proxy_thread.detach();
  std::list<std::thread> odin_worker_threads;
  for(size_t i = 0; i < worker_concurrency; ++i) {
    odin_worker_threads.emplace_back(valhalla::odin::run_service, config);
    odin_worker_threads.back().detach();
  }

  //tyr layer
  std::thread tyr_proxy_thread(std::bind(&proxy_t::forward, proxy_t(context, tyr_proxy + "_in", tyr_proxy + "_out")));
  tyr_proxy_thread.detach();
  std::list<std::thread> tyr_worker_threads;
  for(size_t i = 0; i < worker_concurrency; ++i) {
    tyr_worker_threads.emplace_back(valhalla::tyr::run_service, config);
    tyr_worker_threads.back().detach();
  }

  //TODO: add multipoint accumulator

  //wait forever (or for interrupt)
  server_thread.join();

  return 0;
}

