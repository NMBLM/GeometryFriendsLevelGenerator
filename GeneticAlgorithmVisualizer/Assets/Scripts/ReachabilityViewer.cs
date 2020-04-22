using System.Collections;
using System.Collections.Generic;
using GeometryFriends;
using GeometryFriends.LevelGenerator;
using GeometryFriends.WithGS;
using UnityEngine;
using UnityEngine.UI;
using Random = System.Random;
public class ReachabilityViewer : MonoBehaviour
{

    [SerializeField] private Material unreachableMaterial;
    [SerializeField] private Material platformMaterial;
    [SerializeField] private Material rectangleReachMaterial;
    [SerializeField] private Material circleReachMaterial;
    [SerializeField] private Material cooperativeReachMaterial;
    [SerializeField] private Material bothReachMaterial;
    [SerializeField] private Material collectibleMaterial;
    [SerializeField] private GameObject gridBlockPrefab;
    [SerializeField] private float granularity = 16f;

    
    public LevelDNA level;
    
    //public OldReachHeuristic h;
    public AreaHeuristic h;
    
    public Random random;

    public GAController GC;
    // Start is called before the first frame update
    [SerializeField] private int currentN = 0;
    void Start()
    {
        /** /
        random = new Random();
        var chromosome = new LevelChromosome();
        Debug.Log(chromosome.ToString());
        level = chromosome.GetLevelDNA();
        //level = new LevelDNA(random, TmpFit, init: true);
        //level = new LevelDNA(random, TmpFit, init: false);
        
        Debug.Log("Level: " + level.Description());
        h = new OldReachHeuristic(blockSize:granularity);
        h.CalculateFitness(level);
        h.CellGridToBlockGrid();
        CreateGrid();
        
        //Debug.Log(level.Description());
        /** /
        level = GATestWorld.LevelOne();
        //level = GATestWorld.LevelTwo();
        
        level = GATestWorld.LevelTest();
        
        //h = new OldReachHeuristic(blockSize:granularity);
        h = new AreaHeuristic(TestSpecifications.LevelOne());
        h.CalculateFitness(level);
        h.CellGridToBlockGrid();
        CreateGrid();
        /**/
        
        GC = new GAController();
    }

    // Update is called once per frame
    void Update()
    {
        /** /
        if ( false && Input.GetKeyUp(KeyCode.R))
        {
            foreach (Transform child in transform)
            {
                if (child != this.transform)
                {
                    Destroy(child.gameObject);
                }
            }
            var chromosome = new LevelChromosome();
            Debug.Log(chromosome.ToString());
            level = chromosome.GetLevelDNA();
            //level = new LevelDNA(random, TmpFit, init: true);
            Debug.Log("Level: " + level.Description());
            //h = new OldReachHeuristic(blockSize:granularity);
            h = new AreaHeuristic(TestSpecifications.LevelOne());

            h.CalculateFitness(level);
            h.CellGridToBlockGrid();

            CreateGrid();
        
            //Debug.Log(level.Description());
        }
        /**/

        /**/
        if (Input.GetKeyUp(KeyCode.O))
        {
            currentN -= 1;
            if (currentN < 0) currentN = 0;
            GC.ShowNPopulation(currentN);
            Debug.Log("Viewing: " + currentN);
        }
        if (Input.GetKeyUp(KeyCode.P))
        {
            currentN += 1;
            
            if (!GC.ShowNPopulation(currentN)) currentN -= 1;
            Debug.Log("Viewing: " + currentN);
        }
        if (Input.GetKeyUp(KeyCode.N))
        {
            GC.NextGen();
        }
        /**/
    }

    public void ViewBest(LevelChromosome best)
    {
        foreach (Transform child in transform)
        {
            if (child != this.transform)
            {
                Destroy(child.gameObject);
            }
        }
        Debug.Log("Fitness : " + best.Fitness);
        level = best.GetLevelDNA();
        Debug.Log("Level: " + level.Description() + "\n" + best.ToString());
        h = new AreaHeuristic(TestSpecifications.LevelOne());
        //h = new OldReachHeuristic(blockSize:granularity);
        h.CalculateFitness(level);
        h.CellGridToBlockGrid();
        CreateGrid();
    }
    public float TmpFit(int index)
    {
        return -1.0f;
    }

    public void CreateGrid()
    {
        for (int i = 0; i < h.xGridLen; i++)
        {
            for (int j = 0; j < h.yGridLen; j++)
            {
                var block = Instantiate(gridBlockPrefab, new Vector3(0.5f*i, -0.5f*j, 0), Quaternion.identity);
                block.transform.parent = this.gameObject.transform;
                var mat = block.GetComponent<Renderer>();
                switch (h.grid[i,j])
                {
                    case BlockType.Unreachable:
                        mat.material = unreachableMaterial;
                        break;
                    case BlockType.Platform:
                        mat.material = platformMaterial;
                        break;
                    case BlockType.RectangleCanReach:
                        mat.material = rectangleReachMaterial;
                        break;
                    case BlockType.CircleCanReach:
                        mat.material = circleReachMaterial;
                        mat.material.color = (float)(h.cellGrid[i,j].jumpStrength+16)/40 * Color.yellow;
                        break;
                    case BlockType.CooperativeCanReach:
                        mat.material = cooperativeReachMaterial;
                        mat.material.color = (float)(h.cellGrid[i,j].jumpStrength+16)/40 * Color.cyan;
                        break;
                    case BlockType.BothCanReach:
                        mat.material = bothReachMaterial;
                        break;
                }
            }
        }
        
        int x = (int) ((level.rectangleSpawn.position.X - 40)/ h.blockSize)  + 2;
        int y = (int) ((level.rectangleSpawn.position.Y - 40)/ h.blockSize)  + 2;
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                var recSpawnBlock = 
                    Instantiate(gridBlockPrefab, new Vector3(0.5f*x + 0.5f *i, -0.5f*y - 0.5f *j, -0.5f), Quaternion.identity);
                recSpawnBlock.transform.parent = this.gameObject.transform;
                var recSpawnMat = recSpawnBlock.GetComponent<Renderer>();
                recSpawnMat.material = rectangleReachMaterial;
            }
        }
        
        x = (int) ((level.circleSpawn.position.X - 40)/ h.blockSize)  + 2;
        y = (int) ((level.circleSpawn.position.Y - 40)/ h.blockSize)  + 2;
        for (int i = 0; i < 80/h.blockSize; i++)
        {
            for (int j = 0; j < 80/h.blockSize; j++)
            {
                var circleSpawnBlock =
                    Instantiate(gridBlockPrefab, new Vector3(0.5f*x + 0.5f *i, -0.5f*y - 0.5f *j, -0.5f), Quaternion.identity);
                circleSpawnBlock.transform.parent = this.gameObject.transform;
                var circleSpawnMat = circleSpawnBlock.GetComponent<Renderer>();
                circleSpawnMat.material = circleReachMaterial;
            }
        }

        foreach (var col in level.collectibles)
        {
            x = (int) ((col.position.X - 40)/ h.blockSize)  + 2;
            y = (int) ((col.position.Y - 40)/ h.blockSize)  + 2;
            var collectibleBlock =
                Instantiate(gridBlockPrefab, new Vector3(0.5f*x, -0.5f*y, -0.5f), Quaternion.identity);
            collectibleBlock.transform.parent = this.gameObject.transform;
            var circleSpawnMat = collectibleBlock.GetComponent<Renderer>();
            circleSpawnMat.material = collectibleMaterial;
        }
    }
}
